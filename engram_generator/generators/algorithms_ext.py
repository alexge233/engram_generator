"""Extended algorithm generators -- sorting traces, graph algorithms, DP.

10 generators across tiers 3-5 covering concrete algorithm execution
traces on small inputs with step-by-step state tracking.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Merge Sort Trace (tier 4)
# ---------------------------------------------------------------------------

@register
class MergeSortTraceGenerator(StepGenerator):
    """Trace merge sort on a small array.

    Recursively splits the array, then merges sorted halves.
    Shows each split and merge step with comparison count.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "merge_sort_trace"

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
            Short task description string.
        """
        return "trace merge sort on the array"

    def _merge(self, left: list[int], right: list[int],
               steps: list[str]) -> tuple[list[int], int]:
        """Merge two sorted arrays, recording steps and comparisons.

        Args:
            left: Left sorted subarray.
            right: Right sorted subarray.
            steps: Step log to append to.

        Returns:
            Tuple of (merged_array, comparison_count).
        """
        result: list[int] = []
        i = j = 0
        comps = 0
        while i < len(left) and j < len(right):
            comps += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        steps.append(f"merge {left} + {right} -> {result}")
        return result, comps

    def _merge_sort(self, arr: list[int],
                    steps: list[str]) -> tuple[list[int], int]:
        """Recursively merge sort, logging splits and merges.

        Args:
            arr: Input array.
            steps: Step log to append to.

        Returns:
            Tuple of (sorted_array, total_comparisons).
        """
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        steps.append(f"split {arr} -> {arr[:mid]}, {arr[mid:]}")
        left, c1 = self._merge_sort(arr[:mid], steps)
        right, c2 = self._merge_sort(arr[mid:], steps)
        merged, c3 = self._merge(left, right, steps)
        return merged, c1 + c2 + c3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a merge sort trace problem.

        Args:
            difficulty: Controls array size (6-8 elements).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(3 + difficulty, 8)
        mag = min(10 + difficulty * 5, 50)
        arr = [self._rng.randint(1, mag) for _ in range(n)]

        steps: list[str] = []
        sorted_arr, total_comps = self._merge_sort(arr, steps)

        problem = f"merge sort {arr}"
        return problem, {
            "arr": arr, "sorted": sorted_arr,
            "steps": steps, "comparisons": total_comps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the sorted array and comparison count.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        return (
            f"sorted: {sd['sorted']}, "
            f"comparisons: {sd['comparisons']}"
        )


# ---------------------------------------------------------------------------
# 2. Quicksort Partition (tier 4)
# ---------------------------------------------------------------------------

@register
class QuicksortPartitionGenerator(StepGenerator):
    """Trace Lomuto partition on an array.

    Picks the last element as pivot, traces swap operations,
    and shows the partitioned array with the pivot in place.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quicksort_partition"

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
            Short task description string.
        """
        return "trace Lomuto partition on the array"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lomuto partition trace problem.

        Args:
            difficulty: Controls array size and element range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(5 + difficulty // 2, 8)
        mag = min(10 + difficulty * 5, 50)
        arr = [self._rng.randint(1, mag) for _ in range(n)]

        # Lomuto partition
        a = arr[:]
        pivot = a[-1]
        i = -1
        swaps: list[str] = []
        comps = 0
        for j in range(len(a) - 1):
            comps += 1
            if a[j] <= pivot:
                i += 1
                if i != j:
                    swaps.append(f"swap a[{i}]={a[i]} <-> a[{j}]={a[j]}")
                    a[i], a[j] = a[j], a[i]
        # Place pivot
        i += 1
        if i != len(a) - 1:
            swaps.append(f"swap a[{i}]={a[i]} <-> pivot={a[-1]}")
            a[i], a[-1] = a[-1], a[i]

        problem = f"Lomuto partition {arr}, pivot={pivot}"
        return problem, {
            "arr": arr, "pivot": pivot, "pivot_idx": i,
            "partitioned": a, "swaps": swaps,
            "comparisons": comps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"pivot = {sd['pivot']}"]
        steps.extend(sd["swaps"])
        steps.append(f"pivot placed at index {sd['pivot_idx']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the partitioned array.

        Args:
            sd: Solution data.

        Returns:
            Partitioned array and comparison count.
        """
        return (
            f"partitioned: {sd['partitioned']}, "
            f"comparisons: {sd['comparisons']}"
        )


# ---------------------------------------------------------------------------
# 3. Binary Search Trace (tier 3)
# ---------------------------------------------------------------------------

@register
class BinarySearchTraceGenerator(StepGenerator):
    """Trace binary search on a sorted array.

    Shows lo, hi, mid at each step, indicates which half is eliminated,
    and reports whether the target is found.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "binary_search_trace"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "trace binary search for the target"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a binary search trace problem.

        Creates a sorted array and a target that may or may not exist.

        Args:
            difficulty: Controls array size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(6 + difficulty, 12)
        values = sorted(self._rng.sample(range(1, n * 5), n))

        # Target: sometimes in array, sometimes not
        if self._rng.random() < 0.7:
            target = self._rng.choice(values)
        else:
            target = self._rng.randint(1, n * 5)

        # Trace
        lo, hi = 0, len(values) - 1
        trace: list[str] = []
        found_idx = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            trace.append(f"lo={lo}, hi={hi}, mid={mid}, a[mid]={values[mid]}")
            if values[mid] == target:
                found_idx = mid
                break
            elif values[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1

        problem = f"binary search {values}, target={target}"
        return problem, {
            "arr": values, "target": target,
            "trace": trace, "found_idx": found_idx,
            "steps_count": len(trace),
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
        """Return search result.

        Args:
            sd: Solution data.

        Returns:
            Found index or not-found message.
        """
        if sd["found_idx"] >= 0:
            return (
                f"found at index {sd['found_idx']}, "
                f"steps: {sd['steps_count']}"
            )
        return f"not found, steps: {sd['steps_count']}"


# ---------------------------------------------------------------------------
# 4. Dijkstra Trace (tier 5)
# ---------------------------------------------------------------------------

@register
class DijkstraTraceGenerator(StepGenerator):
    """Trace Dijkstra's shortest-path algorithm on a small weighted graph.

    Shows priority queue state, distance updates, and final shortest
    distances from the source to all vertices.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dijkstra_trace"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bfs_order"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "trace Dijkstra's algorithm from the source"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Dijkstra trace problem on a small graph.

        Constructs a connected graph with 4-5 nodes and positive weights,
        then runs Dijkstra from node 0.

        Args:
            difficulty: Controls graph size and weight range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 4 if difficulty <= 4 else 5
        max_w = min(3 + difficulty * 2, 15)

        # Build adjacency list ensuring connectivity
        adj: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
        # Chain: 0->1->2->...->n-1
        for i in range(n - 1):
            w = self._rng.randint(1, max_w)
            adj[i].append((i + 1, w))
            adj[i + 1].append((i, w))
        # Add random edges
        extra = self._rng.randint(1, min(3, n))
        for _ in range(extra):
            u = self._rng.randint(0, n - 1)
            v = self._rng.randint(0, n - 1)
            if u != v:
                w = self._rng.randint(1, max_w)
                adj[u].append((v, w))
                adj[v].append((u, w))

        # Dijkstra from 0
        INF = 10**9
        dist = [INF] * n
        dist[0] = 0
        visited = [False] * n
        trace: list[str] = []

        for _ in range(n):
            # Pick unvisited with min dist
            u = -1
            for i in range(n):
                if not visited[i] and (u == -1 or dist[i] < dist[u]):
                    u = i
            if u == -1 or dist[u] == INF:
                break
            visited[u] = True
            trace.append(f"visit {u}, dist={dist[u]}")
            for v, w in adj[u]:
                if not visited[v] and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    trace.append(f"  update dist[{v}] = {dist[v]}")

        # Format edges
        edges: list[str] = []
        seen_edges: set[tuple[int, int]] = set()
        for u in range(n):
            for v, w in adj[u]:
                key = (min(u, v), max(u, v))
                if key not in seen_edges:
                    seen_edges.add(key)
                    edges.append(f"{u}-{v}:{w}")

        problem = f"Dijkstra from 0, edges: {', '.join(edges)}"
        return problem, {
            "n": n, "edges": edges,
            "dist": dist[:n], "trace": trace,
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
        """Return final shortest distances.

        Args:
            sd: Solution data.

        Returns:
            Distance array string.
        """
        return f"dist = {sd['dist']}"


# ---------------------------------------------------------------------------
# 5. Kruskal Trace (tier 5)
# ---------------------------------------------------------------------------

@register
class KruskalTraceGenerator(StepGenerator):
    """Trace Kruskal's MST algorithm on a small weighted graph.

    Sorts edges by weight, processes each with union-find logic,
    and shows which edges are added to the MST.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kruskal_trace"

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
            Short task description string.
        """
        return "trace Kruskal's MST algorithm"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Kruskal MST trace problem.

        Builds a connected graph with distinct edge weights,
        then traces Kruskal's algorithm with union-find.

        Args:
            difficulty: Controls node count and weight range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 4 if difficulty <= 3 else 5
        max_w = min(5 + difficulty * 2, 20)

        # Build edges ensuring connectivity
        edges: list[tuple[int, int, int]] = []
        for i in range(n - 1):
            w = self._rng.randint(1, max_w)
            edges.append((w, i, i + 1))
        # Extra edges
        for i in range(n):
            for j in range(i + 2, n):
                if self._rng.random() < 0.4:
                    w = self._rng.randint(1, max_w)
                    edges.append((w, i, j))

        # Sort by weight
        edges.sort()

        # Union-Find
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        mst_edges: list[tuple[int, int, int]] = []
        trace: list[str] = []
        total_weight = 0

        for w, u, v in edges:
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
                mst_edges.append((w, u, v))
                total_weight += w
                trace.append(f"add {u}-{v} (w={w})")
            else:
                trace.append(f"skip {u}-{v} (w={w}), cycle")

        edge_strs = [f"{u}-{v}:{w}" for w, u, v in edges]
        problem = f"Kruskal MST, edges: {', '.join(edge_strs)}"
        return problem, {
            "edges": edge_strs, "trace": trace,
            "mst": [f"{u}-{v}:{w}" for w, u, v in mst_edges],
            "total_weight": total_weight,
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
        """Return MST edges and total weight.

        Args:
            sd: Solution data.

        Returns:
            MST result string.
        """
        return (
            f"MST: {sd['mst']}, "
            f"weight: {sd['total_weight']}"
        )


# ---------------------------------------------------------------------------
# 6. DP Knapsack Trace (tier 5)
# ---------------------------------------------------------------------------

@register
class DPKnapsackTraceGenerator(StepGenerator):
    """Trace 0/1 knapsack DP table construction.

    Fills the DP table row by row for 3-5 items with small capacity,
    then traces back to find the selected items.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dp_knapsack_trace"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["memoisation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "trace the 0/1 knapsack DP table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a knapsack DP trace problem.

        Args:
            difficulty: Controls number of items and capacity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_items = min(3 + difficulty // 3, 5)
        max_w = min(3 + difficulty, 8)
        cap = self._rng.randint(max_w, max_w + 4)

        items: list[tuple[int, int]] = []
        for _ in range(n_items):
            w = self._rng.randint(1, max_w)
            v = self._rng.randint(1, max_w * 2)
            items.append((v, w))

        # Build DP table
        dp = [[0] * (cap + 1) for _ in range(n_items + 1)]
        for i in range(1, n_items + 1):
            v_i, w_i = items[i - 1]
            for c in range(cap + 1):
                dp[i][c] = dp[i - 1][c]
                if w_i <= c:
                    dp[i][c] = max(dp[i][c], v_i + dp[i - 1][c - w_i])

        opt_val = dp[n_items][cap]

        # Traceback
        selected: list[int] = []
        c = cap
        for i in range(n_items, 0, -1):
            if dp[i][c] != dp[i - 1][c]:
                selected.append(i)
                c -= items[i - 1][1]
        selected.reverse()

        # Build trace steps (compact)
        trace: list[str] = []
        for i in range(1, n_items + 1):
            row = dp[i][: cap + 1]
            trace.append(f"item {i} (v={items[i-1][0]},w={items[i-1][1]}): {row}")
        trace.append(f"traceback: items {selected}")

        items_str = ", ".join(f"(v={v},w={w})" for v, w in items)
        problem = f"knapsack: items=[{items_str}], cap={cap}"
        return problem, {
            "items": items, "cap": cap, "opt_val": opt_val,
            "selected": selected, "trace": trace,
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
        """Return optimal value and selected items.

        Args:
            sd: Solution data.

        Returns:
            Knapsack solution string.
        """
        return (
            f"max value = {sd['opt_val']}, "
            f"items: {sd['selected']}"
        )


# ---------------------------------------------------------------------------
# 7. Hash Chaining (tier 4)
# ---------------------------------------------------------------------------

@register
class HashChainingGenerator(StepGenerator):
    """Insert keys into a hash table with chaining.

    Uses h(k) = k mod m. Shows the chain at each bucket after all
    insertions and counts collisions.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hash_chaining"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hash_table_ops"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "insert keys into hash table with chaining"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a hash chaining problem.

        Args:
            difficulty: Controls number of keys and table size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        m = self._rng.choice([5, 7, 11])
        n_keys = min(4 + difficulty, 8)
        keys = [self._rng.randint(1, 50 + difficulty * 10) for _ in range(n_keys)]

        table: dict[int, list[int]] = {i: [] for i in range(m)}
        collisions = 0
        trace: list[str] = []
        for k in keys:
            bucket = k % m
            if table[bucket]:
                collisions += 1
            table[bucket].append(k)
            trace.append(f"h({k}) = {k} mod {m} = {bucket}")

        # Final state
        final: list[str] = []
        for i in range(m):
            if table[i]:
                final.append(f"[{i}]: {table[i]}")
            else:
                final.append(f"[{i}]: empty")

        problem = f"hash table m={m}, keys={keys}"
        return problem, {
            "m": m, "keys": keys, "trace": trace,
            "final": final, "collisions": collisions,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["trace"] + sd["final"]

    def _create_answer(self, sd: dict) -> str:
        """Return collision count and table summary.

        Args:
            sd: Solution data.

        Returns:
            Collision count string.
        """
        return f"collisions = {sd['collisions']}"


# ---------------------------------------------------------------------------
# 8. Heap Sort Trace (tier 4)
# ---------------------------------------------------------------------------

@register
class HeapSortTraceGenerator(StepGenerator):
    """Trace heap sort: build max-heap, then extract-max repeatedly.

    Shows the heap array state after each heapify and extraction step.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "heap_sort_trace"

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
            Short task description string.
        """
        return "trace heap sort on the array"

    def _sift_down(self, arr: list[int], n: int, i: int) -> None:
        """Sift down element at index i in a max-heap.

        Args:
            arr: Heap array (modified in place).
            n: Heap size.
            i: Index to sift down.
        """
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._sift_down(arr, n, largest)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a heap sort trace problem.

        Args:
            difficulty: Controls array size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(5 + difficulty // 2, 8)
        mag = min(10 + difficulty * 5, 50)
        arr = [self._rng.randint(1, mag) for _ in range(n)]
        original = arr[:]

        trace: list[str] = []

        # Build max-heap
        heap = arr[:]
        for i in range(len(heap) // 2 - 1, -1, -1):
            self._sift_down(heap, len(heap), i)
        trace.append(f"build heap: {heap}")

        # Extract max repeatedly
        size = len(heap)
        for _ in range(size - 1):
            heap[0], heap[size - 1] = heap[size - 1], heap[0]
            size -= 1
            self._sift_down(heap, size, 0)
            trace.append(f"extract: {heap[:size]} | sorted: {heap[size:]}")

        problem = f"heap sort {original}"
        return problem, {
            "original": original, "sorted": heap,
            "trace": trace,
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
        """Return the sorted array.

        Args:
            sd: Solution data.

        Returns:
            Sorted array string.
        """
        return f"sorted: {sd['sorted']}"


# ---------------------------------------------------------------------------
# 9. Counting Sort (tier 3)
# ---------------------------------------------------------------------------

@register
class CountingSortGenerator(StepGenerator):
    """Trace counting sort on a small array.

    Counts occurrences, computes prefix sums, places elements into
    output, and shows the count array and final output.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "counting_sort"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "trace counting sort on the array"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a counting sort trace problem.

        Args:
            difficulty: Controls array size and value range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(5 + difficulty, 10)
        max_val = min(3 + difficulty, 9)
        arr = [self._rng.randint(0, max_val) for _ in range(n)]

        # Count
        count = [0] * (max_val + 1)
        for x in arr:
            count[x] += 1

        # Prefix sum
        prefix = count[:]
        for i in range(1, len(prefix)):
            prefix[i] += prefix[i - 1]

        # Stable placement (right to left)
        output = [0] * n
        work_prefix = prefix[:]
        for x in reversed(arr):
            work_prefix[x] -= 1
            output[work_prefix[x]] = x

        problem = f"counting sort {arr}, range [0, {max_val}]"
        return problem, {
            "arr": arr, "max_val": max_val,
            "count": count, "prefix": prefix,
            "output": output,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"count: {sd['count']}",
            f"prefix sum: {sd['prefix']}",
            f"place elements right-to-left",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the sorted array.

        Args:
            sd: Solution data.

        Returns:
            Sorted output string.
        """
        return f"sorted: {sd['output']}"


# ---------------------------------------------------------------------------
# 10. Radix Sort (tier 4)
# ---------------------------------------------------------------------------

@register
class RadixSortGenerator(StepGenerator):
    """Trace LSD radix sort on a small array of integers.

    Sorts by each digit position from least significant to most
    significant, showing the array state after each pass.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "radix_sort"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["counting_sort"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "trace LSD radix sort on the array"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a radix sort trace problem.

        Args:
            difficulty: Controls array size and number of digits.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_digits = min(2 + difficulty // 3, 3)
        lo = 10 ** (n_digits - 1) if n_digits > 1 else 0
        hi = 10 ** n_digits - 1
        n = min(5 + difficulty // 2, 8)
        arr = [self._rng.randint(lo, hi) for _ in range(n)]

        current = arr[:]
        trace: list[str] = []
        max_val = max(current) if current else 0
        num_passes = len(str(max_val)) if max_val > 0 else 1

        for d in range(num_passes):
            # Counting sort by digit d
            buckets: list[list[int]] = [[] for _ in range(10)]
            for x in current:
                digit = (x // (10 ** d)) % 10
                buckets[digit].append(x)
            current = []
            for b in buckets:
                current.extend(b)
            trace.append(f"digit {d} (10^{d}): {current}")

        problem = f"radix sort {arr}"
        return problem, {
            "arr": arr, "sorted": current,
            "trace": trace, "passes": num_passes,
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
        """Return the sorted array.

        Args:
            sd: Solution data.

        Returns:
            Sorted array and pass count.
        """
        return f"sorted: {sd['sorted']}, passes: {sd['passes']}"
