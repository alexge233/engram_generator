"""Systems and networking generators.

8 generators across tiers 4-5 covering relational algebra, database
normalisation, SQL equivalence, OS scheduling, page replacement,
subnet calculation, consistent hashing, and vector clocks.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper classes
# ---------------------------------------------------------------------------

class _Table:
    """A small in-memory table with named columns and row data.

    Attributes:
        columns: Column names.
        rows: List of tuples representing rows.
    """

    def __init__(self, columns: list[str],
                 rows: list[tuple]) -> None:
        """Initialise the table.

        Args:
            columns: Column header names.
            rows: Data rows as tuples.
        """
        self.columns = columns
        self.rows = rows

    def select(self, col: str, value) -> "_Table":
        """Return rows where col equals value.

        Args:
            col: Column name to filter on.
            value: Required value.

        Returns:
            New table with matching rows.
        """
        idx = self.columns.index(col)
        filtered = [r for r in self.rows if r[idx] == value]
        return _Table(self.columns, filtered)

    def project(self, cols: list[str]) -> "_Table":
        """Return table with only the named columns.

        Args:
            cols: Column names to keep.

        Returns:
            New table with projected columns.
        """
        idxs = [self.columns.index(c) for c in cols]
        projected = list({tuple(r[i] for i in idxs) for r in self.rows})
        projected.sort()
        return _Table(cols, projected)

    def join(self, other: "_Table", on: str) -> "_Table":
        """Natural join on a shared column.

        Args:
            other: Table to join with.
            on: Shared column name.

        Returns:
            Joined table.
        """
        li = self.columns.index(on)
        ri = other.columns.index(on)
        new_cols = list(self.columns) + [
            c for c in other.columns if c != on
        ]
        joined = []
        for lr in self.rows:
            for rr in other.rows:
                if lr[li] == rr[ri]:
                    row = lr + tuple(
                        rr[j] for j in range(len(rr)) if j != ri
                    )
                    joined.append(row)
        return _Table(new_cols, joined)

    def compact(self) -> str:
        """Format table as a compact string.

        Returns:
            Pipe-separated header and rows.
        """
        hdr = "|".join(self.columns)
        rows_str = "; ".join(
            "|".join(str(v) for v in r) for r in self.rows
        )
        return f"[{hdr}]: {rows_str}"


class _ProcessInfo:
    """A process descriptor for scheduling simulation.

    Attributes:
        pid: Process identifier.
        arrival: Arrival time.
        burst: CPU burst time.
    """

    def __init__(self, pid: str, arrival: int, burst: int) -> None:
        """Initialise the process.

        Args:
            pid: Process name.
            arrival: Arrival time.
            burst: Burst duration.
        """
        self.pid = pid
        self.arrival = arrival
        self.burst = burst


# ---------------------------------------------------------------------------
# 1. Relational Algebra (tier 4)
# ---------------------------------------------------------------------------

@register
class RelationalAlgebraGenerator(StepGenerator):
    """Evaluate select, project, or join on small tables.

    Generates tables with 2-4 rows and 2-3 columns, then applies
    a relational algebra operation and shows the resulting table.
    """

    _NAMES = ["Alice", "Bob", "Cara", "Dan", "Eve"]
    _DEPTS = ["CS", "EE", "Math", "Bio"]
    _CITIES = ["NYC", "LA", "CHI", "SF"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "relational_algebra"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_operations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "evaluate relational algebra expression"

    def _make_table(self, n_rows: int) -> _Table:
        """Build a random employee table.

        Args:
            n_rows: Number of rows.

        Returns:
            A table with columns id, name, dept.
        """
        names = self._rng.sample(self._NAMES, n_rows)
        depts = [self._rng.choice(self._DEPTS) for _ in range(n_rows)]
        rows = [(i + 1, names[i], depts[i]) for i in range(n_rows)]
        return _Table(["id", "name", "dept"], rows)

    def _make_dept_table(self) -> _Table:
        """Build a department-city lookup table.

        Returns:
            A table with columns dept, city.
        """
        depts = self._rng.sample(self._DEPTS, min(3, len(self._DEPTS)))
        cities = self._rng.sample(self._CITIES, len(depts))
        rows = [(d, c) for d, c in zip(depts, cities)]
        return _Table(["dept", "city"], rows)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a relational algebra problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_rows = min(2 + difficulty // 2, 4)
        tbl = self._make_table(n_rows)
        op = self._rng.choice(["select", "project", "join"])

        if op == "select":
            dept = self._rng.choice(self._DEPTS)
            result = tbl.select("dept", dept)
            expr = f"SELECT(dept={dept})"
            steps = [
                f"scan {len(tbl.rows)} rows",
                f"keep rows where dept={dept}",
                f"result has {len(result.rows)} rows",
            ]
        elif op == "project":
            cols = self._rng.sample(["id", "name", "dept"], 2)
            result = tbl.project(cols)
            expr = f"PROJECT({','.join(cols)})"
            steps = [
                f"keep columns {cols}",
                f"remove duplicates",
                f"result has {len(result.rows)} rows",
            ]
        else:
            dept_tbl = self._make_dept_table()
            result = tbl.join(dept_tbl, "dept")
            expr = f"JOIN(emp, dept_loc, on=dept)"
            steps = [
                f"match rows on dept",
                f"combine columns",
                f"result has {len(result.rows)} rows",
            ]
            problem = f"{tbl.compact()} {expr} with {dept_tbl.compact()}"
            return problem, {
                "steps": steps,
                "result": result,
            }

        problem = f"{tbl.compact()} {expr}"
        return problem, {"steps": steps, "result": result}

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the operation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the resulting table.

        Args:
            solution_data: All computed solution information.

        Returns:
            Compact table string.
        """
        return solution_data["result"].compact()


# ---------------------------------------------------------------------------
# 2. Normalisation (tier 5)
# ---------------------------------------------------------------------------

@register
class NormalisationGenerator(StepGenerator):
    """Identify the highest normal form of a relation given functional dependencies.

    Given a table schema and a set of functional dependencies, determine
    whether the relation is in 1NF, 2NF, 3NF, or BCNF.
    """

    _TEMPLATES: list[dict] = [
        {
            "schema": "R(A, B, C)",
            "key": "{A, B}",
            "fds": ["A,B -> C"],
            "analysis": "no partial or transitive deps",
            "form": "BCNF",
        },
        {
            "schema": "R(A, B, C)",
            "key": "{A, B}",
            "fds": ["A,B -> C", "B -> C"],
            "analysis": "B->C is partial dep on key {A,B}",
            "form": "1NF",
        },
        {
            "schema": "R(A, B, C, D)",
            "key": "{A}",
            "fds": ["A -> B", "A -> C", "C -> D"],
            "analysis": "C->D is transitive (A->C->D)",
            "form": "2NF",
        },
        {
            "schema": "R(A, B, C)",
            "key": "{A}",
            "fds": ["A -> B", "A -> C"],
            "analysis": "all FDs have superkey on LHS",
            "form": "BCNF",
        },
        {
            "schema": "R(A, B, C, D)",
            "key": "{A, B}",
            "fds": ["A,B -> C", "A,B -> D", "C -> D"],
            "analysis": "C->D transitive via non-key attr",
            "form": "2NF",
        },
        {
            "schema": "R(A, B, C)",
            "key": "{A}",
            "fds": ["A -> B", "B -> C"],
            "analysis": "B->C transitive dep (A->B->C)",
            "form": "2NF",
        },
        {
            "schema": "R(A, B, C, D)",
            "key": "{A, B}",
            "fds": ["A,B -> C,D", "A -> C"],
            "analysis": "A->C partial dep on {A,B}",
            "form": "1NF",
        },
        {
            "schema": "R(A, B, C)",
            "key": "{A, B}",
            "fds": ["A,B -> C"],
            "analysis": "single non-key attr determined by full key",
            "form": "BCNF",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "normalisation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["relational_algebra"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "identify highest normal form from functional dependencies"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a normalisation identification problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]
        fds_str = "; ".join(tmpl["fds"])
        problem = f"{tmpl['schema']}, key={tmpl['key']}, FDs: {fds_str}"
        return problem, {
            "schema": tmpl["schema"],
            "key": tmpl["key"],
            "fds": tmpl["fds"],
            "analysis": tmpl["analysis"],
            "form": tmpl["form"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate normalisation analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings showing FD analysis.
        """
        return [
            f"key={solution_data['key']}",
            f"check FDs: {'; '.join(solution_data['fds'])}",
            solution_data["analysis"],
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the highest normal form.

        Args:
            solution_data: All computed solution information.

        Returns:
            Normal form label.
        """
        return solution_data["form"]


# ---------------------------------------------------------------------------
# 3. SQL Equivalence (tier 5)
# ---------------------------------------------------------------------------

@register
class SQLEquivalenceGenerator(StepGenerator):
    """Determine if two simple SQL-like queries produce the same result.

    Given two select-project-join queries and sample data, evaluate
    both and compare the results.
    """

    _TEMPLATES: list[dict] = [
        {
            "data": "[id|v]: 1|a; 2|b; 3|a",
            "q1": "SELECT v FROM R WHERE v='a'",
            "q2": "SELECT v FROM R WHERE id<3 AND v='a'",
            "r1": "{a, a}",
            "r2": "{a}",
            "equiv": False,
            "reason": "Q1 returns 2 rows, Q2 returns 1",
        },
        {
            "data": "[id|v]: 1|x; 2|y; 3|x",
            "q1": "SELECT DISTINCT v FROM R",
            "q2": "SELECT v FROM R GROUP BY v",
            "r1": "{x, y}",
            "r2": "{x, y}",
            "equiv": True,
            "reason": "both produce distinct values",
        },
        {
            "data": "[id|v]: 1|a; 2|b",
            "q1": "SELECT * FROM R WHERE v='a' OR v='b'",
            "q2": "SELECT * FROM R",
            "r1": "{(1,a),(2,b)}",
            "r2": "{(1,a),(2,b)}",
            "equiv": True,
            "reason": "condition covers all existing values",
        },
        {
            "data": "[id|v]: 1|a; 2|a; 3|b",
            "q1": "SELECT id FROM R WHERE v='a'",
            "q2": "SELECT id FROM R WHERE id<=2",
            "r1": "{1, 2}",
            "r2": "{1, 2}",
            "equiv": True,
            "reason": "both select ids 1 and 2 on this data",
        },
        {
            "data": "[id|v|w]: 1|a|X; 2|b|Y; 3|a|Y",
            "q1": "SELECT v,w FROM R WHERE v='a'",
            "q2": "SELECT v,w FROM R WHERE w='X'",
            "r1": "{(a,X),(a,Y)}",
            "r2": "{(a,X)}",
            "equiv": False,
            "reason": "Q1 returns 2 rows, Q2 returns 1",
        },
        {
            "data": "[id|v]: 1|a; 2|b; 3|c",
            "q1": "SELECT v FROM R WHERE id>1",
            "q2": "SELECT v FROM R WHERE v<>'a'",
            "r1": "{b, c}",
            "r2": "{b, c}",
            "equiv": True,
            "reason": "both exclude only row with id=1,v=a",
        },
        {
            "data": "[id|v]: 1|a; 2|a",
            "q1": "SELECT COUNT(*) FROM R",
            "q2": "SELECT COUNT(DISTINCT v) FROM R",
            "r1": "2",
            "r2": "1",
            "equiv": False,
            "reason": "COUNT(*)=2 but COUNT(DISTINCT v)=1",
        },
        {
            "data": "[id|v]: 1|a; 2|b; 3|c",
            "q1": "SELECT * FROM R ORDER BY id",
            "q2": "SELECT * FROM R ORDER BY v",
            "r1": "{(1,a),(2,b),(3,c)}",
            "r2": "{(1,a),(2,b),(3,c)}",
            "equiv": True,
            "reason": "alphabetical order matches id order here",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sql_equivalence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["relational_algebra"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "determine if two SQL queries are equivalent on sample data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an SQL equivalence problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]
        problem = (
            f"data: {tmpl['data']}; "
            f"Q1: {tmpl['q1']}; Q2: {tmpl['q2']}"
        )
        return problem, {
            "q1": tmpl["q1"],
            "q2": tmpl["q2"],
            "r1": tmpl["r1"],
            "r2": tmpl["r2"],
            "equiv": tmpl["equiv"],
            "reason": tmpl["reason"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate evaluation steps for both queries.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings comparing query results.
        """
        return [
            f"Q1 result: {solution_data['r1']}",
            f"Q2 result: {solution_data['r2']}",
            solution_data["reason"],
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return equivalence verdict.

        Args:
            solution_data: All computed solution information.

        Returns:
            EQUIVALENT or NOT EQUIVALENT.
        """
        return "EQUIVALENT" if solution_data["equiv"] else "NOT EQUIVALENT"


# ---------------------------------------------------------------------------
# 4. Scheduling Algorithm (tier 4)
# ---------------------------------------------------------------------------

@register
class SchedulingAlgorithmGenerator(StepGenerator):
    """Simulate FIFO, SJF, or Round-Robin scheduling on 3-5 processes.

    Generates a set of processes with arrival and burst times, runs
    the chosen algorithm, and computes average waiting time.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "scheduling_algorithm"

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
        return "simulate CPU scheduling algorithm"

    def _make_processes(self, difficulty: int) -> list[_ProcessInfo]:
        """Generate a list of processes.

        Args:
            difficulty: Controls number of processes and burst range.

        Returns:
            List of process descriptors.
        """
        n = min(3 + difficulty // 3, 5)
        procs = []
        for i in range(n):
            arrival = self._rng.randint(0, min(difficulty, 4))
            burst = self._rng.randint(1, min(3 + difficulty, 8))
            procs.append(_ProcessInfo(f"P{i}", arrival, burst))
        return procs

    def _fifo(self, procs: list[_ProcessInfo]) -> tuple[list[str], float]:
        """Simulate FIFO (FCFS) scheduling.

        Args:
            procs: List of processes sorted by arrival.

        Returns:
            Tuple of (steps, average_wait_time).
        """
        ordered = sorted(procs, key=lambda p: (p.arrival, p.pid))
        time = 0
        steps = []
        total_wait = 0
        for p in ordered:
            start = max(time, p.arrival)
            wait = start - p.arrival
            total_wait += wait
            steps.append(f"{p.pid}: start={start} wait={wait}")
            time = start + p.burst
        avg = round(total_wait / len(ordered), 2)
        return steps, avg

    def _sjf(self, procs: list[_ProcessInfo]) -> tuple[list[str], float]:
        """Simulate non-preemptive SJF scheduling.

        Args:
            procs: List of processes.

        Returns:
            Tuple of (steps, average_wait_time).
        """
        remaining = list(procs)
        time = 0
        steps = []
        total_wait = 0
        done = []
        while remaining:
            available = [p for p in remaining if p.arrival <= time]
            if not available:
                time = min(p.arrival for p in remaining)
                continue
            available.sort(key=lambda p: (p.burst, p.arrival))
            p = available[0]
            remaining.remove(p)
            wait = time - p.arrival
            total_wait += wait
            steps.append(f"{p.pid}: start={time} wait={wait}")
            time += p.burst
            done.append(p)
        avg = round(total_wait / len(procs), 2)
        return steps, avg

    def _round_robin(self, procs: list[_ProcessInfo],
                     quantum: int) -> tuple[list[str], float]:
        """Simulate Round-Robin scheduling.

        Args:
            procs: List of processes.
            quantum: Time quantum.

        Returns:
            Tuple of (steps, average_wait_time).
        """
        queue = []
        remaining = {p.pid: p.burst for p in procs}
        arrived = {p.pid: False for p in procs}
        sorted_procs = sorted(procs, key=lambda p: (p.arrival, p.pid))
        time = 0
        steps = []
        finish_time = {}

        # Seed the queue with processes arriving at time 0.
        for p in sorted_procs:
            if p.arrival <= time and not arrived[p.pid]:
                queue.append(p.pid)
                arrived[p.pid] = True

        while queue or any(not arrived[p.pid] for p in sorted_procs):
            if not queue:
                time = min(
                    p.arrival for p in sorted_procs if not arrived[p.pid]
                )
                for p in sorted_procs:
                    if p.arrival <= time and not arrived[p.pid]:
                        queue.append(p.pid)
                        arrived[p.pid] = True
            pid = queue.pop(0)
            run = min(remaining[pid], quantum)
            steps.append(f"t={time}: {pid} runs {run}")
            time += run
            remaining[pid] -= run
            # Check for new arrivals during this burst.
            for p in sorted_procs:
                if p.arrival <= time and not arrived[p.pid]:
                    queue.append(p.pid)
                    arrived[p.pid] = True
            if remaining[pid] > 0:
                queue.append(pid)
            else:
                finish_time[pid] = time

        total_wait = 0
        for p in sorted_procs:
            turnaround = finish_time.get(p.pid, time) - p.arrival
            wait = turnaround - p.burst
            total_wait += max(0, wait)
        avg = round(total_wait / len(procs), 2)
        return steps, avg

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a scheduling problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        procs = self._make_processes(difficulty)
        algo = self._rng.choice(["FIFO", "SJF", "RR"])

        proc_str = ", ".join(
            f"{p.pid}(arr={p.arrival},burst={p.burst})" for p in procs
        )

        if algo == "FIFO":
            steps, avg = self._fifo(procs)
            problem = f"{algo}: {proc_str}"
        elif algo == "SJF":
            steps, avg = self._sjf(procs)
            problem = f"{algo}: {proc_str}"
        else:
            quantum = self._rng.randint(1, 3)
            steps, avg = self._round_robin(procs, quantum)
            problem = f"RR(q={quantum}): {proc_str}"

        return problem, {"steps": steps, "avg_wait": avg}

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the scheduling simulation steps.

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
        return f"avg_wait={solution_data['avg_wait']}"


# ---------------------------------------------------------------------------
# 5. Page Replacement (tier 4)
# ---------------------------------------------------------------------------

@register
class PageReplacementGenerator(StepGenerator):
    """Simulate LRU or FIFO page replacement on a reference string.

    Generates a page reference string and a frame count, then
    simulates the replacement policy and counts page faults.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "page_replacement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "simulate page replacement algorithm"

    def _make_reference_string(self, difficulty: int) -> list[int]:
        """Generate a page reference string.

        Args:
            difficulty: Controls length and page range.

        Returns:
            List of page numbers.
        """
        length = min(6 + difficulty * 2, 14)
        max_page = min(3 + difficulty, 7)
        return [self._rng.randint(0, max_page) for _ in range(length)]

    def _fifo_simulate(self, refs: list[int],
                       frames: int) -> tuple[list[str], int]:
        """Simulate FIFO page replacement.

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

    def _lru_simulate(self, refs: list[int],
                      frames: int) -> tuple[list[str], int]:
        """Simulate LRU page replacement.

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
        """Generate a page replacement problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        refs = self._make_reference_string(difficulty)
        frames = self._rng.randint(2, 4)
        algo = self._rng.choice(["FIFO", "LRU"])

        if algo == "FIFO":
            steps, faults = self._fifo_simulate(refs, frames)
        else:
            steps, faults = self._lru_simulate(refs, frames)

        ref_str = ",".join(str(r) for r in refs)
        problem = f"{algo} frames={frames} refs=[{ref_str}]"
        return problem, {"steps": steps, "faults": faults}

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the simulation trace.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings for each reference.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the page fault count.

        Args:
            solution_data: All computed solution information.

        Returns:
            Fault count string.
        """
        return f"faults={solution_data['faults']}"


# ---------------------------------------------------------------------------
# 6. Subnet Calculation (tier 4)
# ---------------------------------------------------------------------------

@register
class SubnetCalculateGenerator(StepGenerator):
    """Compute network address, broadcast, host range, and host count from IP/CIDR.

    Given an IP address and CIDR prefix length, perform the subnet
    calculation using binary arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "subnet_calculate"

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
        return "compute subnet details from IP/CIDR"

    def _generate_ip_cidr(self, difficulty: int) -> tuple[list[int], int]:
        """Generate a random IP address and CIDR prefix.

        Args:
            difficulty: Controls prefix length variety.

        Returns:
            Tuple of (octets, prefix_length).
        """
        octets = [self._rng.randint(1, 254) for _ in range(4)]
        # Higher difficulty uses more unusual prefix lengths.
        if difficulty <= 3:
            prefix = self._rng.choice([8, 16, 24])
        elif difficulty <= 6:
            prefix = self._rng.choice([20, 22, 24, 25, 26])
        else:
            prefix = self._rng.choice([19, 21, 23, 27, 28, 29])
        return octets, prefix

    def _compute_subnet(self, octets: list[int],
                        prefix: int) -> dict:
        """Compute subnet parameters.

        Args:
            octets: Four IP octets.
            prefix: CIDR prefix length.

        Returns:
            Dict with network, broadcast, first_host, last_host, num_hosts.
        """
        ip_int = 0
        for o in octets:
            ip_int = (ip_int << 8) | o

        mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
        network_int = ip_int & mask
        broadcast_int = network_int | (~mask & 0xFFFFFFFF)
        num_hosts = max(0, (1 << (32 - prefix)) - 2)

        def to_dotted(val: int) -> str:
            return ".".join(
                str((val >> (24 - 8 * i)) & 0xFF) for i in range(4)
            )

        network = to_dotted(network_int)
        broadcast = to_dotted(broadcast_int)
        first_host = to_dotted(network_int + 1) if num_hosts > 0 else network
        last_host = to_dotted(broadcast_int - 1) if num_hosts > 0 else broadcast

        return {
            "network": network,
            "broadcast": broadcast,
            "first_host": first_host,
            "last_host": last_host,
            "num_hosts": num_hosts,
            "mask": to_dotted(mask),
        }

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a subnet calculation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        octets, prefix = self._generate_ip_cidr(difficulty)
        ip_str = ".".join(str(o) for o in octets)
        result = self._compute_subnet(octets, prefix)
        problem = f"{ip_str}/{prefix}"
        return problem, result

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate subnet calculation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings showing mask, network, broadcast computation.
        """
        return [
            f"mask={solution_data['mask']}",
            f"network={solution_data['network']}",
            f"broadcast={solution_data['broadcast']}",
            f"hosts={solution_data['first_host']}-{solution_data['last_host']}",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the subnet details.

        Args:
            solution_data: All computed solution information.

        Returns:
            Compact subnet summary.
        """
        return (
            f"net={solution_data['network']} "
            f"bcast={solution_data['broadcast']} "
            f"hosts={solution_data['num_hosts']}"
        )


# ---------------------------------------------------------------------------
# 7. Consistent Hashing (tier 5)
# ---------------------------------------------------------------------------

@register
class ConsistentHashingGenerator(StepGenerator):
    """Determine which node serves a key on a hash ring.

    Places nodes on a hash ring (0-359), hashes a key, and finds the
    first node clockwise. Optionally simulates adding or removing a node.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "consistent_hashing"

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
        return "consistent hashing: find serving node on hash ring"

    def _build_ring(self, difficulty: int) -> tuple[dict[str, int], int, str]:
        """Build a hash ring with nodes and a key.

        Args:
            difficulty: Controls number of nodes.

        Returns:
            Tuple of (node_positions, key_hash, operation).
        """
        n_nodes = min(3 + difficulty // 2, 6)
        positions = sorted(self._rng.sample(range(0, 360, 10), n_nodes))
        nodes = {f"N{i}": positions[i] for i in range(n_nodes)}
        key_hash = self._rng.randint(0, 359)

        if difficulty >= 5:
            op = self._rng.choice(["add", "remove"])
        else:
            op = "lookup"

        return nodes, key_hash, op

    def _find_node(self, nodes: dict[str, int],
                   key_hash: int) -> str:
        """Find the serving node for a key hash.

        Args:
            nodes: Node name to position mapping.
            key_hash: Hash value of the key.

        Returns:
            Name of the serving node.
        """
        sorted_items = sorted(nodes.items(), key=lambda x: x[1])
        for name, pos in sorted_items:
            if pos >= key_hash:
                return name
        # Wrap around to first node.
        return sorted_items[0][0]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a consistent hashing problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        nodes, key_hash, op = self._build_ring(difficulty)
        serving_before = self._find_node(nodes, key_hash)

        steps = [
            f"ring: {', '.join(f'{n}@{p}' for n, p in sorted(nodes.items(), key=lambda x: x[1]))}",
            f"key hash={key_hash}",
            f"clockwise -> {serving_before}",
        ]

        if op == "add":
            new_pos = self._rng.choice(
                [p for p in range(0, 360, 10) if p not in nodes.values()]
            )
            new_name = f"N{len(nodes)}"
            nodes_after = dict(nodes)
            nodes_after[new_name] = new_pos
            serving_after = self._find_node(nodes_after, key_hash)
            steps.append(f"add {new_name}@{new_pos}")
            steps.append(f"after add -> {serving_after}")
            answer = f"before={serving_before} after_add={serving_after}"
        elif op == "remove":
            removable = [n for n in nodes if n != serving_before]
            if not removable:
                removable = list(nodes.keys())
            rm_name = self._rng.choice(removable)
            nodes_after = {n: p for n, p in nodes.items() if n != rm_name}
            if nodes_after:
                serving_after = self._find_node(nodes_after, key_hash)
            else:
                serving_after = "NONE"
            steps.append(f"remove {rm_name}")
            steps.append(f"after remove -> {serving_after}")
            answer = f"before={serving_before} after_rm={serving_after}"
        else:
            answer = f"node={serving_before}"

        ring_str = " ".join(
            f"{n}@{p}" for n, p in sorted(nodes.items(), key=lambda x: x[1])
        )
        problem = f"ring=[{ring_str}] key_hash={key_hash} op={op}"
        return problem, {"steps": steps, "answer": answer}

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the hash ring lookup steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the serving node(s).

        Args:
            solution_data: All computed solution information.

        Returns:
            Serving node result.
        """
        return solution_data["answer"]


# ---------------------------------------------------------------------------
# 8. Vector Clock Update (tier 5)
# ---------------------------------------------------------------------------

@register
class VectorClockUpdateGenerator(StepGenerator):
    """Update vector clocks for events across 2-3 processes.

    Generates a sequence of local, send, and receive events, updates
    vector clocks according to the standard rules, and determines
    causal ordering between two events.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vector_clock_update"

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
        return "update vector clocks and determine causal ordering"

    def _generate_events(self, difficulty: int) -> tuple[int, list[dict]]:
        """Generate a sequence of events across processes.

        Args:
            difficulty: Controls number of processes and events.

        Returns:
            Tuple of (n_processes, event_list).
        """
        n_procs = 2 if difficulty <= 4 else 3
        n_events = min(4 + difficulty, 8)
        events = []
        for _ in range(n_events):
            proc = self._rng.randint(0, n_procs - 1)
            kind = self._rng.choice(["local", "send", "receive"])
            if kind == "send":
                dest = self._rng.choice(
                    [p for p in range(n_procs) if p != proc]
                )
                events.append({"proc": proc, "type": "send", "dest": dest})
            elif kind == "receive":
                # Find a pending send from another process.
                senders = [
                    e for e in events
                    if e["type"] == "send" and e["dest"] == proc
                    and not e.get("received", False)
                ]
                if senders:
                    sender_event = senders[-1]
                    sender_event["received"] = True
                    events.append({
                        "proc": proc, "type": "receive",
                        "from_proc": sender_event["proc"],
                        "sender_idx": events.index(sender_event),
                    })
                else:
                    events.append({"proc": proc, "type": "local"})
            else:
                events.append({"proc": proc, "type": "local"})
        return n_procs, events

    def _simulate_clocks(self, n_procs: int,
                         events: list[dict]) -> tuple[list[str], list[list[int]]]:
        """Simulate vector clock updates.

        Args:
            n_procs: Number of processes.
            events: Event sequence.

        Returns:
            Tuple of (steps, list_of_clock_snapshots).
        """
        clocks = [[0] * n_procs for _ in range(n_procs)]
        steps = []
        snapshots = []

        for i, evt in enumerate(events):
            p = evt["proc"]
            clocks[p][p] += 1

            if evt["type"] == "send":
                steps.append(
                    f"e{i}: P{p} send to P{evt['dest']} "
                    f"VC={list(clocks[p])}"
                )
                evt["clock_snapshot"] = list(clocks[p])
            elif evt["type"] == "receive":
                sender_clock = events[evt["sender_idx"]].get(
                    "clock_snapshot", [0] * n_procs
                )
                for j in range(n_procs):
                    clocks[p][j] = max(clocks[p][j], sender_clock[j])
                steps.append(
                    f"e{i}: P{p} recv from P{evt['from_proc']} "
                    f"VC={list(clocks[p])}"
                )
            else:
                steps.append(
                    f"e{i}: P{p} local VC={list(clocks[p])}"
                )

            snapshots.append(list(clocks[p]))

        return steps, snapshots

    def _compare_events(self, snap_a: list[int],
                        snap_b: list[int]) -> str:
        """Determine causal ordering between two vector clock snapshots.

        Args:
            snap_a: Vector clock of first event.
            snap_b: Vector clock of second event.

        Returns:
            Ordering result string.
        """
        a_leq_b = all(a <= b for a, b in zip(snap_a, snap_b))
        b_leq_a = all(b <= a for a, b in zip(snap_a, snap_b))
        a_lt_b = a_leq_b and snap_a != snap_b
        b_lt_a = b_leq_a and snap_a != snap_b

        if a_lt_b:
            return "a -> b (a happens-before b)"
        if b_lt_a:
            return "b -> a (b happens-before a)"
        if snap_a == snap_b:
            return "a = b (same event)"
        return "a || b (concurrent)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a vector clock problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_procs, events = self._generate_events(difficulty)
        steps, snapshots = self._simulate_clocks(n_procs, events)

        # Pick two events to compare.
        if len(snapshots) >= 2:
            idxs = self._rng.sample(range(len(snapshots)), 2)
            idxs.sort()
            ordering = self._compare_events(
                snapshots[idxs[0]], snapshots[idxs[1]]
            )
            steps.append(
                f"compare e{idxs[0]} {snapshots[idxs[0]]} vs "
                f"e{idxs[1]} {snapshots[idxs[1]]}"
            )
        else:
            ordering = "insufficient events"

        evt_str = "; ".join(
            f"e{i}:P{e['proc']},{e['type']}" for i, e in enumerate(events)
        )
        problem = f"{n_procs} procs, events: {evt_str}"
        return problem, {"steps": steps, "ordering": ordering}

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the vector clock update steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the causal ordering result.

        Args:
            solution_data: All computed solution information.

        Returns:
            Ordering verdict.
        """
        return solution_data["ordering"]
