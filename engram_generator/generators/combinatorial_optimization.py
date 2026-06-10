"""Combinatorial optimisation generators.

8 generators across tiers 4-6 covering TSP heuristics, assignment,
matching, scheduling, knapsack, set cover, bin packing, and integer
programming.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class TSPNearestNeighborGenerator(StepGenerator):
    """Solve TSP using the nearest-neighbor heuristic.

    Starting from city 0, always visit the nearest unvisited city.
    Computes the total tour length on 4-6 cities with integer
    distance matrices.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tsp_nearest_neighbor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["shortest_path"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "TSP nearest neighbor heuristic"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a TSP instance and solve with nearest-neighbor.

        Args:
            difficulty: Controls city count (4-6).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(4 + difficulty // 3, 6)
        # Symmetric distance matrix
        dist = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d = self._rng.randint(1, 5 + difficulty * 2)
                dist[i][j] = d
                dist[j][i] = d

        # Nearest-neighbor tour from city 0
        visited = [0]
        unvisited = set(range(1, n))
        total = 0
        trace = []
        current = 0
        while unvisited:
            nearest = min(unvisited, key=lambda c: dist[current][c])
            cost = dist[current][nearest]
            total += cost
            trace.append(f"{current}->{nearest} (d={cost})")
            current = nearest
            visited.append(current)
            unvisited.remove(current)
        # Return to start
        ret_cost = dist[current][0]
        total += ret_cost
        trace.append(f"{current}->0 (d={ret_cost})")
        visited.append(0)

        dist_rows = "; ".join(
            "[" + ",".join(str(d) for d in row) + "]"
            for row in dist
        )
        problem = f"{n} cities, dist=[{dist_rows}]"
        return problem, {
            "n": n, "tour": visited, "trace": trace,
            "total": total,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the tour and its cost.

        Args:
            sd: Solution data.

        Returns:
            Tour sequence and total distance.
        """
        tour_str = "->".join(str(c) for c in sd["tour"])
        return f"tour: {tour_str}, cost={sd['total']}"


@register
class AssignmentProblemGenerator(StepGenerator):
    """Solve a 3x3 assignment problem.

    Applies a simplified Hungarian method: row reduction, column
    reduction, then greedy assignment on the reduced cost matrix.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "assignment_problem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "solve assignment problem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 3x3 cost matrix and find minimum cost assignment.

        Args:
            difficulty: Controls cost range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 3
        cost = [
            [self._rng.randint(1, 5 + difficulty * 2) for _ in range(n)]
            for _ in range(n)
        ]

        # Row reduction
        reduced = [row[:] for row in cost]
        row_mins = []
        for i in range(n):
            m = min(reduced[i])
            row_mins.append(m)
            for j in range(n):
                reduced[i][j] -= m

        # Column reduction
        col_mins = []
        for j in range(n):
            m = min(reduced[i][j] for i in range(n))
            col_mins.append(m)
            for i in range(n):
                reduced[i][j] -= m

        # Brute-force optimal assignment on 3x3
        from itertools import permutations
        best_cost = float("inf")
        best_perm = (0, 1, 2)
        for perm in permutations(range(n)):
            c = sum(cost[i][perm[i]] for i in range(n))
            if c < best_cost:
                best_cost = c
                best_perm = perm

        assignment = [(i, best_perm[i]) for i in range(n)]

        def fmt(M: list[list[int]]) -> str:
            """Format a matrix as a string."""
            rows = [",".join(str(v) for v in r) for r in M]
            return "[" + "],[".join(rows) + "]"

        problem = f"cost=[{fmt(cost)}]. Find min cost assignment."
        return problem, {
            "cost": cost, "reduced": reduced,
            "row_mins": row_mins, "col_mins": col_mins,
            "assignment": assignment, "min_cost": best_cost,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        def fmt(M: list[list[int]]) -> str:
            """Format a matrix as a string."""
            rows = [",".join(str(v) for v in r) for r in M]
            return "[" + "],[".join(rows) + "]"

        steps = [
            f"row reduce (mins={sd['row_mins']})",
            f"col reduce (mins={sd['col_mins']})",
            f"reduced=[{fmt(sd['reduced'])}]",
        ]
        for i, j in sd["assignment"]:
            steps.append(f"assign row {i}->col {j} (cost={sd['cost'][i][j]})")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the optimal assignment and cost.

        Args:
            sd: Solution data.

        Returns:
            Assignment pairs and total cost.
        """
        pairs = ", ".join(f"({i},{j})" for i, j in sd["assignment"])
        return f"assignment: {pairs}, cost={sd['min_cost']}"


@register
class BipartiteMatchingGenerator(StepGenerator):
    """Find maximum matching in a bipartite graph.

    Uses augmenting path search on a small bipartite graph
    (3-5 nodes per side) to build a maximum matching.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "matching_bipartite"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bipartite_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "maximum bipartite matching"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bipartite graph and find maximum matching.

        Args:
            difficulty: Controls graph size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_left = min(3 + difficulty // 3, 5)
        n_right = n_left

        # Generate random edges
        edges = []
        for u in range(n_left):
            n_edges = self._rng.randint(1, min(3, n_right))
            targets = self._rng.sample(range(n_right), n_edges)
            for v in targets:
                edges.append((u, v))
        edges = list(set(edges))

        # Build adjacency for left side
        adj = {u: [] for u in range(n_left)}
        for u, v in edges:
            adj[u].append(v)

        # Hungarian-style augmenting paths
        match_right = [-1] * n_right

        def augment(u: int, visited: set) -> bool:
            """Try to find an augmenting path from left node u."""
            for v in adj[u]:
                if v in visited:
                    continue
                visited.add(v)
                if match_right[v] == -1 or augment(match_right[v], visited):
                    match_right[v] = u
                    return True
            return False

        trace = []
        for u in range(n_left):
            visited = set()
            found = augment(u, visited)
            trace.append(
                f"try L{u}: {'matched' if found else 'no path'}"
            )

        matching = []
        for v in range(n_right):
            if match_right[v] != -1:
                matching.append((match_right[v], v))
        matching.sort()

        edge_str = ", ".join(f"L{u}-R{v}" for u, v in edges)
        problem = (
            f"left=0..{n_left - 1}, right=0..{n_right - 1}, "
            f"edges=[{edge_str}]"
        )
        return problem, {
            "trace": trace, "matching": matching,
            "size": len(matching),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = list(sd["trace"])
        for u, v in sd["matching"]:
            steps.append(f"match: L{u}-R{v}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Extract the maximum matching size.

        Args:
            sd: Solution data.

        Returns:
            Matching size and pairs.
        """
        pairs = ", ".join(f"L{u}-R{v}" for u, v in sd["matching"])
        return f"matching size={sd['size']}: {pairs}"


@register
class JobSchedulingGenerator(StepGenerator):
    """Minimise total weighted completion time using Smith's rule.

    Sorts jobs by w_i / p_i in decreasing order and computes
    total weighted completion time sum(w_i * C_i).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "job_scheduling"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "job scheduling (Smith's rule)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a job scheduling problem and solve with Smith's rule.

        Args:
            difficulty: Controls job count and value range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(3 + difficulty // 2, 6)
        jobs = []
        for i in range(n):
            w = self._rng.randint(1, 5 + difficulty)
            p = self._rng.randint(1, 5 + difficulty)
            jobs.append({"id": i, "w": w, "p": p, "ratio": round(w / p, 4)})

        # Smith's rule: sort by w/p descending
        order = sorted(jobs, key=lambda j: j["ratio"], reverse=True)

        # Compute weighted completion time
        trace = []
        total_wc = 0
        c = 0
        for j in order:
            c += j["p"]
            wc = j["w"] * c
            total_wc += wc
            trace.append(
                f"job {j['id']}: w={j['w']}, p={j['p']}, "
                f"w/p={j['ratio']}, C={c}, wC={wc}"
            )

        job_str = ", ".join(
            f"(w={j['w']},p={j['p']})" for j in jobs
        )
        problem = f"{n} jobs: {job_str}. Minimise sum(w_i*C_i)."
        return problem, {
            "jobs": jobs, "order": [j["id"] for j in order],
            "trace": trace, "total_wc": total_wc,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        order_str = "->".join(str(i) for i in sd["order"])
        return [f"order: {order_str}"] + sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the minimum weighted completion time.

        Args:
            sd: Solution data.

        Returns:
            Total weighted completion time.
        """
        return f"sum(w_i*C_i)={sd['total_wc']}"


@register
class FractionalKnapsackGenerator(StepGenerator):
    """Solve the fractional knapsack problem greedily.

    Sorts items by value/weight ratio in decreasing order and
    fills the knapsack, taking fractions of the last item if needed.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "knapsack_fractional"

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
            Short task description.
        """
        return "fractional knapsack"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a fractional knapsack problem.

        Args:
            difficulty: Controls item count and value range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(3 + difficulty // 2, 6)
        items = []
        for i in range(n):
            v = self._rng.randint(2, 8 + difficulty * 2)
            w = self._rng.randint(1, 5 + difficulty)
            items.append({
                "id": i, "v": v, "w": w,
                "ratio": round(v / w, 4),
            })
        capacity = self._rng.randint(
            sum(it["w"] for it in items) // 3,
            sum(it["w"] for it in items) * 2 // 3,
        )
        capacity = max(capacity, 1)

        # Sort by v/w descending
        order = sorted(items, key=lambda it: it["ratio"], reverse=True)

        trace = []
        total_value = 0.0
        remaining = capacity
        for it in order:
            if remaining <= 0:
                break
            if it["w"] <= remaining:
                frac = 1.0
                taken = it["w"]
            else:
                frac = round(remaining / it["w"], 4)
                taken = remaining
            val_gain = round(frac * it["v"], 4)
            total_value += val_gain
            remaining -= taken
            trace.append(
                f"item {it['id']}: v={it['v']}, w={it['w']}, "
                f"ratio={it['ratio']}, frac={frac}, gain={val_gain}"
            )

        total_value = round(total_value, 4)
        item_str = ", ".join(
            f"(v={it['v']},w={it['w']})" for it in items
        )
        problem = f"{n} items: {item_str}, capacity={capacity}"
        return problem, {
            "trace": trace, "total_value": total_value,
            "capacity": capacity,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the maximum achievable value.

        Args:
            sd: Solution data.

        Returns:
            Total value obtained.
        """
        return f"max value={sd['total_value']}"


@register
class SetCoverGreedyGenerator(StepGenerator):
    """Solve set cover using the greedy algorithm.

    At each step, picks the set covering the most uncovered
    elements until all elements are covered.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "set_cover_greedy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["minimum_spanning_tree"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "greedy set cover"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a set cover problem and solve greedily.

        Args:
            difficulty: Controls universe and set sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_elements = min(4 + difficulty, 8)
        n_sets = min(3 + difficulty // 2, 6)
        universe = set(range(n_elements))

        # Generate sets ensuring full coverage
        sets = []
        for i in range(n_sets):
            size = self._rng.randint(1, max(2, n_elements // 2))
            s = set(self._rng.sample(range(n_elements), size))
            sets.append(s)

        # Ensure coverage: distribute any uncovered elements
        covered = set()
        for s in sets:
            covered |= s
        for e in universe - covered:
            idx = self._rng.randint(0, n_sets - 1)
            sets[idx].add(e)

        # Greedy algorithm
        uncovered = set(universe)
        chosen = []
        trace = []
        while uncovered:
            best_idx = -1
            best_count = 0
            for i in range(n_sets):
                if i in [c for c, _ in chosen]:
                    continue
                count = len(sets[i] & uncovered)
                if count > best_count:
                    best_count = count
                    best_idx = i
            if best_idx == -1:
                break
            newly_covered = sets[best_idx] & uncovered
            chosen.append((best_idx, sorted(newly_covered)))
            trace.append(
                f"pick S{best_idx}={sorted(sets[best_idx])}, "
                f"covers {sorted(newly_covered)}"
            )
            uncovered -= newly_covered

        sets_str = ", ".join(
            f"S{i}={sorted(s)}" for i, s in enumerate(sets)
        )
        problem = (
            f"U={{0..{n_elements - 1}}}, {sets_str}. "
            f"Greedy set cover."
        )
        return problem, {
            "sets": [sorted(s) for s in sets],
            "chosen": chosen, "trace": trace,
            "n_chosen": len(chosen),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the number of sets used.

        Args:
            sd: Solution data.

        Returns:
            Sets chosen and count.
        """
        ids = ", ".join(f"S{i}" for i, _ in sd["chosen"])
        return f"{sd['n_chosen']} sets: {ids}"


@register
class BinPackingGenerator(StepGenerator):
    """Pack items into bins using first-fit decreasing.

    Sorts items in decreasing order of size, then places each item
    in the first bin that has enough remaining capacity.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bin_packing"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "first-fit decreasing bin packing"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bin packing problem and solve with FFD.

        Args:
            difficulty: Controls item count and size range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(4 + difficulty, 8)
        bin_cap = self._rng.randint(5 + difficulty, 10 + difficulty * 2)
        items = [
            self._rng.randint(1, bin_cap) for _ in range(n)
        ]

        # First-fit decreasing
        sorted_items = sorted(items, reverse=True)
        bins = []  # each bin is a list of items
        remaining = []  # remaining capacity per bin
        trace = []

        for item in sorted_items:
            placed = False
            for b_idx in range(len(bins)):
                if remaining[b_idx] >= item:
                    bins[b_idx].append(item)
                    remaining[b_idx] -= item
                    trace.append(
                        f"item {item} -> bin {b_idx} "
                        f"(remaining={remaining[b_idx]})"
                    )
                    placed = True
                    break
            if not placed:
                bins.append([item])
                remaining.append(bin_cap - item)
                trace.append(
                    f"item {item} -> new bin {len(bins) - 1} "
                    f"(remaining={remaining[-1]})"
                )

        problem = (
            f"items={sorted_items}, bin capacity={bin_cap}. "
            f"FFD packing."
        )
        return problem, {
            "items": sorted_items, "bins": bins,
            "trace": trace, "n_bins": len(bins),
            "bin_cap": bin_cap,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the number of bins used.

        Args:
            sd: Solution data.

        Returns:
            Bin count and contents.
        """
        bins_str = "; ".join(
            f"B{i}={b}" for i, b in enumerate(sd["bins"])
        )
        return f"{sd['n_bins']} bins: {bins_str}"


@register
class IntegerProgrammingGenerator(StepGenerator):
    """Solve a small 2-variable ILP by branch-and-bound.

    Solves the LP relaxation, branches on a fractional variable,
    and finds the optimal integer solution.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "integer_programming"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "integer programming (branch and bound)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2-variable ILP and solve by branch-and-bound.

        Args:
            difficulty: Controls coefficient range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c1 = self._rng.randint(1, 3 + difficulty)
        c2 = self._rng.randint(1, 3 + difficulty)

        # Two constraints: a1*x + a2*y <= b
        a1 = self._rng.randint(1, 3)
        a2 = self._rng.randint(1, 3)
        b1 = self._rng.randint(4, 8 + difficulty)
        d1 = self._rng.randint(1, 3)
        d2 = self._rng.randint(1, 3)
        b2 = self._rng.randint(4, 8 + difficulty)

        constraints = [(a1, a2, b1), (d1, d2, b2)]

        # LP relaxation: enumerate integer points for small ILP
        best_obj = -1
        best_x, best_y = 0, 0
        x_max = b1 // a1 + 1 if a1 > 0 else 20
        y_max = b1 // a2 + 1 if a2 > 0 else 20
        x_max = min(x_max, 15)
        y_max = min(y_max, 15)

        feasible_pts = []
        for x in range(x_max + 1):
            for y in range(y_max + 1):
                if (a1 * x + a2 * y <= b1 and d1 * x + d2 * y <= b2):
                    obj = c1 * x + c2 * y
                    feasible_pts.append((x, y, obj))
                    if obj > best_obj:
                        best_obj = obj
                        best_x, best_y = x, y

        # LP relaxation bound (approximate via constraint intersection)
        det = a1 * d2 - a2 * d1
        if det != 0:
            x_lp = round((b1 * d2 - a2 * b2) / det, 4)
            y_lp = round((a1 * b2 - b1 * d1) / det, 4)
            if x_lp >= 0 and y_lp >= 0:
                lp_obj = round(c1 * x_lp + c2 * y_lp, 4)
            else:
                x_lp, y_lp = round(b1 / a1, 4), 0.0
                lp_obj = round(c1 * x_lp, 4)
        else:
            x_lp, y_lp = round(b1 / a1, 4), 0.0
            lp_obj = round(c1 * x_lp, 4)

        # Branch variable
        x_frac = x_lp != int(x_lp)
        branch_var = "x" if x_frac else "y"
        branch_val = x_lp if x_frac else y_lp

        con_str = (
            f"{a1}x+{a2}y<={b1}, {d1}x+{d2}y<={b2}"
        )
        problem = (
            f"max {c1}x+{c2}y s.t. {con_str}, "
            f"x,y>=0, x,y integer"
        )
        return problem, {
            "c": (c1, c2),
            "constraints": constraints,
            "lp_relaxation": (x_lp, y_lp, lp_obj),
            "branch_var": branch_var,
            "branch_val": branch_val,
            "optimal": (best_x, best_y, best_obj),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        x_lp, y_lp, lp_obj = sd["lp_relaxation"]
        bv = sd["branch_var"]
        bval = sd["branch_val"]
        floor_val = math.floor(bval)
        ceil_val = math.ceil(bval)
        return [
            f"LP relaxation: x={x_lp}, y={y_lp}, z={lp_obj}",
            f"branch on {bv}={bval}",
            f"left: {bv}<={floor_val}",
            f"right: {bv}>={ceil_val}",
            f"optimal integer: x={sd['optimal'][0]}, "
            f"y={sd['optimal'][1]}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Extract the optimal integer solution.

        Args:
            sd: Solution data.

        Returns:
            Optimal point and objective value.
        """
        x, y, obj = sd["optimal"]
        return f"max={obj} at ({x},{y})"
