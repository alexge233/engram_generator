"""Deep algorithm generators -- string algorithms, DP variants, graph algorithms.

10 generators across tiers 4-5 covering KMP search, Rabin-Karp, suffix
arrays, matrix chain DP, longest palindrome, quickselect, Tarjan SCC,
A* search, weighted edit distance, and interval scheduling.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# HELPER UTILITIES
# ===================================================================

def _format_array(arr: list) -> str:
    """Format a list as a bracketed string.

    Args:
        arr: List of values.

    Returns:
        String like ``[3, 1, 4, 1]``.
    """
    return "[" + ", ".join(str(x) for x in arr) + "]"


# ===================================================================
# 1. KMP SEARCH (tier 5)
# ===================================================================

@register
class KMPSearchGenerator(StepGenerator):
    """Trace the KMP string search algorithm.

    Builds the failure function (partial match table) for a pattern,
    then shows matching steps against a text.

    Difficulty scaling:
        Difficulty 1-3: pattern length 3, text length 8-10.
        Difficulty 4-6: pattern length 4, text length 10-14.
        Difficulty 7-8: pattern length 5, text length 12-16.

    Prerequisites:
        comparison (tier 0).
    """

    ALPHABET = "abcd"

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kmp_search"

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
            Short task description string.
        """
        return "trace KMP pattern search with failure function"

    def _build_failure(self, pattern: str) -> list[int]:
        """Build the KMP failure function.

        Args:
            pattern: The search pattern.

        Returns:
            Failure function as a list of integers.
        """
        m = len(pattern)
        fail = [0] * m
        k = 0
        for i in range(1, m):
            while k > 0 and pattern[k] != pattern[i]:
                k = fail[k - 1]
            if pattern[k] == pattern[i]:
                k += 1
            fail[i] = k
        return fail

    def _kmp_match(self, text: str, pattern: str,
                   fail: list[int]) -> list[int]:
        """Run KMP matching.

        Args:
            text: The text to search.
            pattern: The pattern to find.
            fail: Precomputed failure function.

        Returns:
            List of match start indices.
        """
        matches: list[int] = []
        j = 0
        for i in range(len(text)):
            while j > 0 and text[i] != pattern[j]:
                j = fail[j - 1]
            if text[i] == pattern[j]:
                j += 1
            if j == len(pattern):
                matches.append(i - len(pattern) + 1)
                j = fail[j - 1]
        return matches

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a KMP search problem.

        Args:
            difficulty: Controls pattern/text sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            plen, tlen = 3, self._rng.randint(8, 10)
        elif difficulty <= 6:
            plen, tlen = 4, self._rng.randint(10, 14)
        else:
            plen, tlen = 5, self._rng.randint(12, 16)

        chars = self.ALPHABET[:min(3 + difficulty // 3, 4)]
        pattern = "".join(self._rng.choice(chars) for _ in range(plen))

        # Ensure at least one match by embedding pattern
        pos = self._rng.randint(0, tlen - plen)
        text_chars = [self._rng.choice(chars) for _ in range(tlen)]
        for i, c in enumerate(pattern):
            text_chars[pos + i] = c
        text = "".join(text_chars)

        fail = self._build_failure(pattern)
        matches = self._kmp_match(text, pattern, fail)

        steps = [
            f"pattern: \"{pattern}\"",
            f"failure function: {fail}",
            f"text: \"{text}\"",
        ]
        for m in matches:
            steps.append(f"match at index {m}")

        problem = f"KMP search for \"{pattern}\" in \"{text}\""
        return problem, {
            "pattern": pattern, "text": text,
            "fail": fail, "matches": matches,
            "steps": steps,
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
        """Return the failure function and match positions.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return (f"failure: {sd['fail']}; "
                f"matches at: {sd['matches']}")


# ===================================================================
# 2. RABIN-KARP (tier 5)
# ===================================================================

@register
class RabinKarpGenerator(StepGenerator):
    """Trace the Rabin-Karp rolling hash search.

    Uses a simple polynomial hash h = sum(c * d^i) mod q.
    Shows hash computation, rolling updates, and match verification.

    Difficulty scaling:
        Difficulty 1-3: pattern length 2, d=256, q=101.
        Difficulty 4-6: pattern length 3, d=256, q=101.
        Difficulty 7-8: pattern length 3-4, d=256, q=101.

    Prerequisites:
        hash_table_ops (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rabin_karp"

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
            Short task description string.
        """
        return "trace Rabin-Karp rolling hash search"

    def _poly_hash(self, s: str, d: int, q: int) -> int:
        """Compute polynomial rolling hash of a string.

        Args:
            s: Input string.
            d: Base for the hash.
            q: Modulus for the hash.

        Returns:
            Hash value.
        """
        h = 0
        for c in s:
            h = (h * d + ord(c)) % q
        return h

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Rabin-Karp search problem.

        Args:
            difficulty: Controls pattern length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        d_base = 256
        q = 101

        if difficulty <= 3:
            plen = 2
        elif difficulty <= 6:
            plen = 3
        else:
            plen = self._rng.choice([3, 4])

        chars = "abcde"[:min(3 + difficulty // 2, 5)]
        pattern = "".join(self._rng.choice(chars) for _ in range(plen))
        tlen = plen + self._rng.randint(4, 8)

        # Embed pattern for at least one match
        pos = self._rng.randint(0, tlen - plen)
        text_list = [self._rng.choice(chars) for _ in range(tlen)]
        for i, c in enumerate(pattern):
            text_list[pos + i] = c
        text = "".join(text_list)

        pat_hash = self._poly_hash(pattern, d_base, q)
        h_mult = pow(d_base, plen - 1, q)

        steps = [
            f"d={d_base}, q={q}",
            f"pattern hash(\"{pattern}\") = {pat_hash}",
        ]
        matches: list[int] = []
        win_hash = self._poly_hash(text[:plen], d_base, q)
        for i in range(len(text) - plen + 1):
            if i > 0:
                old_c = ord(text[i - 1])
                new_c = ord(text[i + plen - 1])
                win_hash = ((win_hash - old_c * h_mult) * d_base + new_c) % q
            cur_win = text[i:i + plen]
            if win_hash == pat_hash:
                if cur_win == pattern:
                    matches.append(i)
                    steps.append(
                        f"i={i}: hash={win_hash} match, verify \"{cur_win}\" = TRUE"
                    )
                else:
                    steps.append(
                        f"i={i}: hash={win_hash} match, verify \"{cur_win}\" = FALSE (spurious)"
                    )

        problem = f"Rabin-Karp: find \"{pattern}\" in \"{text}\""
        return problem, {
            "pattern": pattern, "text": text,
            "pat_hash": pat_hash, "matches": matches,
            "d": d_base, "q": q, "steps": steps,
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
        """Return the pattern hash and match positions.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return (f"hash(\"{sd['pattern']}\") = {sd['pat_hash']}; "
                f"matches at: {sd['matches']}")


# ===================================================================
# 3. SUFFIX ARRAY (tier 5)
# ===================================================================

@register
class SuffixArrayGenerator(StepGenerator):
    """Build the suffix array for a short string.

    Lists all suffixes, sorts them lexicographically, and returns
    the array of starting indices.

    Difficulty scaling:
        Difficulty 1-3: string length 5-6.
        Difficulty 4-6: string length 6-7.
        Difficulty 7-8: string length 7-8.

    Prerequisites:
        sorting (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "suffix_array"

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
        return "build the suffix array for a string"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a suffix array problem.

        Args:
            difficulty: Controls string length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(5, 6)
        elif difficulty <= 6:
            n = self._rng.randint(6, 7)
        else:
            n = self._rng.randint(7, 8)

        chars = "abc"[:min(2 + difficulty // 3, 3)]
        s = "".join(self._rng.choice(chars) for _ in range(n))

        suffixes = [(s[i:], i) for i in range(n)]
        sorted_suffixes = sorted(suffixes, key=lambda x: x[0])
        sa = [idx for _, idx in sorted_suffixes]

        steps = [f"string: \"{s}\""]
        for suf, idx in sorted_suffixes:
            steps.append(f"  [{idx}] \"{suf}\"")
        steps.append(f"suffix array: {sa}")

        problem = f"build suffix array for \"{s}\""
        return problem, {
            "s": s, "sa": sa,
            "sorted_suffixes": [(suf, idx) for suf, idx in sorted_suffixes],
            "steps": steps,
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
        """Return the suffix array.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"SA(\"{sd['s']}\") = {sd['sa']}"


# ===================================================================
# 4. MATRIX CHAIN DP (tier 5)
# ===================================================================

@register
class MatrixChainDPGenerator(StepGenerator):
    """Find minimum multiplications for a matrix chain product.

    Uses DP recurrence m[i][j] = min over k of
    (m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]).

    Difficulty scaling:
        Difficulty 1-3: 3 matrices.
        Difficulty 4-6: 4 matrices.
        Difficulty 7-8: 5 matrices.

    Prerequisites:
        memoisation (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "matrix_chain_dp"

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
        return "find minimum scalar multiplications for a matrix chain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a matrix chain multiplication problem.

        Args:
            difficulty: Controls number of matrices.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            num_matrices = 3
        elif difficulty <= 6:
            num_matrices = 4
        else:
            num_matrices = 5

        # Generate dimensions
        dims = [self._rng.randint(2, 15) for _ in range(num_matrices + 1)]
        n = num_matrices

        # DP
        m = [[0] * n for _ in range(n)]
        s = [[0] * n for _ in range(n)]
        steps: list[str] = [f"dimensions: {dims}"]

        for chain_len in range(2, n + 1):
            for i in range(n - chain_len + 1):
                j = i + chain_len - 1
                m[i][j] = float("inf")
                for k in range(i, j):
                    cost = m[i][k] + m[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                    if cost < m[i][j]:
                        m[i][j] = int(cost)
                        s[i][j] = k
                steps.append(f"m[{i}][{j}] = {m[i][j]} (split at k={s[i][j]})")

        optimal = m[0][n - 1]
        steps.append(f"minimum multiplications = {optimal}")

        matrices = [f"A{i+1}({dims[i]}x{dims[i+1]})" for i in range(n)]
        problem = f"matrix chain: {', '.join(matrices)}"
        return problem, {
            "dims": dims, "n": n,
            "optimal": optimal, "steps": steps,
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
        """Return the minimum number of multiplications.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"minimum scalar multiplications = {sd['optimal']}"


# ===================================================================
# 5. LONGEST PALINDROME (tier 4)
# ===================================================================

@register
class LongestPalindromeGenerator(StepGenerator):
    """Find the longest palindromic substring by expanding around centres.

    Checks each position as a centre for both odd and even length
    palindromes. Tracks the longest found.

    Difficulty scaling:
        Difficulty 1-3: string length 6-8.
        Difficulty 4-6: string length 8-10.
        Difficulty 7-8: string length 10-12.

    Prerequisites:
        comparison (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "longest_palindrome"

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
            Short task description string.
        """
        return "find the longest palindromic substring"

    def _expand(self, s: str, left: int, right: int) -> str:
        """Expand around centre to find palindrome.

        Args:
            s: Input string.
            left: Left index of centre.
            right: Right index of centre.

        Returns:
            Longest palindrome from this centre.
        """
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a longest palindrome problem.

        Args:
            difficulty: Controls string length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(6, 8)
        elif difficulty <= 6:
            n = self._rng.randint(8, 10)
        else:
            n = self._rng.randint(10, 12)

        chars = "abcd"[:min(2 + difficulty // 2, 4)]

        # Embed a palindrome of length 3-5
        pal_len = min(3 + difficulty // 2, 5)
        half = "".join(self._rng.choice(chars) for _ in range(pal_len // 2))
        mid = self._rng.choice(chars) if pal_len % 2 == 1 else ""
        embedded_pal = half + mid + half[::-1]

        s_list = [self._rng.choice(chars) for _ in range(n)]
        start = self._rng.randint(0, max(0, n - len(embedded_pal)))
        for i, c in enumerate(embedded_pal):
            if start + i < n:
                s_list[start + i] = c
        s = "".join(s_list)

        # Find actual longest palindrome
        best = s[0]
        steps: list[str] = [f"string: \"{s}\""]
        for i in range(len(s)):
            odd = self._expand(s, i, i)
            even = self._expand(s, i, i + 1)
            for p in [odd, even]:
                if len(p) > len(best):
                    best = p
                    steps.append(f"centre {i}: found \"{p}\" (len {len(p)})")

        steps.append(f"longest palindrome: \"{best}\" (len {len(best)})")

        problem = f"find longest palindromic substring in \"{s}\""
        return problem, {
            "s": s, "best": best, "length": len(best),
            "steps": steps,
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
        """Return the longest palindromic substring.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"\"{sd['best']}\" (length {sd['length']})"


# ===================================================================
# 6. TOP-K QUICKSELECT (tier 4)
# ===================================================================

@register
class TopKQuickselectGenerator(StepGenerator):
    """Trace partition-based quickselect to find the k-th smallest.

    Uses Lomuto partition, shows each partition step and pivot
    placement until the k-th element is found.

    Difficulty scaling:
        Difficulty 1-3: array of 5-6 elements.
        Difficulty 4-6: array of 6-8 elements.
        Difficulty 7-8: array of 8-10 elements.

    Prerequisites:
        sorting (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "topk_quickselect"

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
        return "find the k-th smallest element using quickselect"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a quickselect problem.

        Args:
            difficulty: Controls array size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(5, 6)
        elif difficulty <= 6:
            n = self._rng.randint(6, 8)
        else:
            n = self._rng.randint(8, 10)

        mag = min(10 + difficulty * 5, 50)
        arr = [self._rng.randint(1, mag) for _ in range(n)]
        k = self._rng.randint(1, n)

        # Simulate quickselect with step logging
        work = list(arr)
        steps: list[str] = [f"array: {_format_array(arr)}, find k={k}"]
        lo, hi = 0, n - 1
        iteration = 0
        while lo < hi and iteration < 20:
            iteration += 1
            pivot = work[hi]
            i = lo
            for j in range(lo, hi):
                if work[j] <= pivot:
                    work[i], work[j] = work[j], work[i]
                    i += 1
            work[i], work[hi] = work[hi], work[i]
            steps.append(
                f"pivot={pivot}, placed at {i}: {_format_array(work[lo:hi+1])}"
            )
            if i == k - 1:
                break
            elif i < k - 1:
                lo = i + 1
            else:
                hi = i - 1

        answer = sorted(arr)[k - 1]
        steps.append(f"k={k} smallest = {answer}")

        problem = f"quickselect k={k} from {_format_array(arr)}"
        return problem, {
            "arr": arr, "k": k, "answer": answer,
            "steps": steps,
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
        """Return the k-th smallest element.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"k={sd['k']} smallest = {sd['answer']}"


# ===================================================================
# 7. TARJAN SCC (tier 5)
# ===================================================================

@register
class TarjanSCCGenerator(StepGenerator):
    """Trace Tarjan's algorithm for strongly connected components.

    Uses discovery time, low-link values, and a stack to identify
    SCCs in a directed graph.

    Difficulty scaling:
        Difficulty 1-3: 4 nodes, 4-5 edges.
        Difficulty 4-6: 5 nodes, 5-7 edges.
        Difficulty 7-8: 6 nodes, 7-9 edges.

    Prerequisites:
        dfs_order (tier 3).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tarjan_scc"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dfs_order"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "find strongly connected components using Tarjan's algorithm"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Tarjan SCC problem.

        Args:
            difficulty: Controls graph size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n, num_edges = 4, self._rng.randint(4, 5)
        elif difficulty <= 6:
            n, num_edges = 5, self._rng.randint(5, 7)
        else:
            n, num_edges = 6, self._rng.randint(7, 9)

        adj: dict[int, list[int]] = {i: [] for i in range(n)}
        edges: set[tuple[int, int]] = set()
        while len(edges) < num_edges:
            u = self._rng.randint(0, n - 1)
            v = self._rng.randint(0, n - 1)
            if u != v and (u, v) not in edges:
                edges.add((u, v))
                adj[u].append(v)

        # Run Tarjan's
        disc = [-1] * n
        low = [-1] * n
        on_stack = [False] * n
        stack: list[int] = []
        sccs: list[list[int]] = []
        timer = [0]
        steps: list[str] = []

        def _strongconnect(u: int) -> None:
            disc[u] = low[u] = timer[0]
            timer[0] += 1
            stack.append(u)
            on_stack[u] = True
            steps.append(f"visit {u}: disc={disc[u]}, low={low[u]}")

            for v in adj[u]:
                if disc[v] == -1:
                    _strongconnect(v)
                    low[u] = min(low[u], low[v])
                elif on_stack[v]:
                    low[u] = min(low[u], disc[v])

            if low[u] == disc[u]:
                scc: list[int] = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    scc.append(w)
                    if w == u:
                        break
                scc.sort()
                sccs.append(scc)
                steps.append(f"SCC found: {scc}")

        for i in range(n):
            if disc[i] == -1:
                _strongconnect(i)

        edge_list = sorted(edges)
        problem = f"Tarjan SCC: {n} nodes, edges {edge_list}"
        return problem, {
            "n": n, "edges": edge_list,
            "sccs": sccs, "steps": steps,
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
        """Return the strongly connected components.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        scc_str = "; ".join(str(s) for s in sd["sccs"])
        return f"SCCs: {scc_str} ({len(sd['sccs'])} components)"


# ===================================================================
# 8. A* SEARCH (tier 5)
# ===================================================================

@register
class AStarSearchGenerator(StepGenerator):
    """Trace A* search on a small weighted graph with heuristic.

    Shows open list (priority queue) state, f(n) = g(n) + h(n),
    and expansion order.

    Difficulty scaling:
        Difficulty 1-3: 4 nodes.
        Difficulty 4-6: 5 nodes.
        Difficulty 7-8: 6 nodes.

    Prerequisites:
        shortest_path (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "a_star_search"

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
            Short task description string.
        """
        return "trace A* search with heuristic on a weighted graph"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an A* search problem.

        Args:
            difficulty: Controls graph size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
        elif difficulty <= 6:
            n = 5
        else:
            n = 6

        # Build connected graph with weights
        adj: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
        # Ensure path from 0 to n-1
        for i in range(n - 1):
            w = self._rng.randint(1, 10)
            adj[i].append((i + 1, w))
            adj[i + 1].append((i, w))

        # Add random edges
        extra = self._rng.randint(1, n - 1)
        for _ in range(extra):
            u = self._rng.randint(0, n - 1)
            v = self._rng.randint(0, n - 1)
            if u != v:
                w = self._rng.randint(1, 10)
                adj[u].append((v, w))

        # Heuristic: distance to goal (admissible)
        goal = n - 1
        h = [max(0, (goal - i) * self._rng.randint(1, 3)) for i in range(n)]
        h[goal] = 0

        # Run A*
        import heapq
        dist = [float("inf")] * n
        dist[0] = 0
        pq: list[tuple[int, int]] = [(h[0], 0)]
        expanded: list[int] = []
        steps: list[str] = [f"h = {h}"]

        while pq:
            f_val, u = heapq.heappop(pq)
            if u in expanded:
                continue
            expanded.append(u)
            g_u = dist[u]
            steps.append(f"expand {u}: g={g_u}, h={h[u]}, f={g_u + h[u]}")
            if u == goal:
                break
            for v, w in adj[u]:
                new_g = g_u + w
                if new_g < dist[v]:
                    dist[v] = new_g
                    heapq.heappush(pq, (new_g + h[v], v))

        shortest = dist[goal] if dist[goal] != float("inf") else -1
        steps.append(f"shortest path to {goal}: {shortest}")

        edge_desc = {u: [(v, w) for v, w in adj[u]] for u in range(n)}
        problem = f"A* from 0 to {goal}, h={h}"
        return problem, {
            "n": n, "goal": goal, "h": h,
            "edges": edge_desc, "shortest": shortest,
            "expanded": expanded, "steps": steps,
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
        """Return the shortest path distance and expansion order.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return (f"shortest = {sd['shortest']}; "
                f"expansion order: {sd['expanded']}")


# ===================================================================
# 9. EDIT DISTANCE VARIANTS (tier 5)
# ===================================================================

@register
class EditDistanceVariantsGenerator(StepGenerator):
    """Compute weighted edit distance with custom operation costs.

    Supports different costs for insert, delete, and substitute.
    Shows the DP table and minimum cost alignment.

    Difficulty scaling:
        Difficulty 1-3: strings of length 3-4, uniform weights.
        Difficulty 4-6: strings of length 4-5, varied weights.
        Difficulty 7-8: strings of length 5-6, varied weights.

    Prerequisites:
        edit_distance (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "edit_distance_variants"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["edit_distance"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute weighted edit distance with custom costs"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a weighted edit distance problem.

        Args:
            difficulty: Controls string length and weight complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            slen = self._rng.randint(3, 4)
            ins_cost, del_cost, sub_cost = 1, 1, 1
        elif difficulty <= 6:
            slen = self._rng.randint(4, 5)
            ins_cost = self._rng.randint(1, 3)
            del_cost = self._rng.randint(1, 3)
            sub_cost = self._rng.randint(1, 3)
        else:
            slen = self._rng.randint(5, 6)
            ins_cost = self._rng.randint(1, 4)
            del_cost = self._rng.randint(1, 4)
            sub_cost = self._rng.randint(2, 5)

        chars = "abcde"
        s1 = "".join(self._rng.choice(chars) for _ in range(slen))
        s2_len = self._rng.randint(max(2, slen - 1), slen + 1)
        s2 = "".join(self._rng.choice(chars) for _ in range(s2_len))

        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i * del_cost
        for j in range(n + 1):
            dp[0][j] = j * ins_cost
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(
                        dp[i - 1][j] + del_cost,
                        dp[i][j - 1] + ins_cost,
                        dp[i - 1][j - 1] + sub_cost,
                    )

        result = dp[m][n]
        steps = [
            f"\"{s1}\" -> \"{s2}\"",
            f"costs: insert={ins_cost}, delete={del_cost}, substitute={sub_cost}",
        ]
        # Show last row
        steps.append(f"dp[{m}] = {dp[m]}")
        steps.append(f"distance = {result}")

        problem = (f"weighted edit distance: \"{s1}\" -> \"{s2}\" "
                   f"(ins={ins_cost}, del={del_cost}, sub={sub_cost})")
        return problem, {
            "s1": s1, "s2": s2, "result": result,
            "ins": ins_cost, "del": del_cost, "sub": sub_cost,
            "steps": steps,
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
        """Return the weighted edit distance.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return (f"d(\"{sd['s1']}\",\"{sd['s2']}\") = {sd['result']} "
                f"(ins={sd['ins']}, del={sd['del']}, sub={sd['sub']})")


# ===================================================================
# 10. INTERVAL SCHEDULING (tier 4)
# ===================================================================

@register
class IntervalSchedulingGenerator(StepGenerator):
    """Solve the interval scheduling maximisation problem.

    Greedy algorithm: sort by finish time, select non-overlapping
    intervals.

    Difficulty scaling:
        Difficulty 1-3: 4-5 intervals.
        Difficulty 4-6: 5-7 intervals.
        Difficulty 7-8: 7-9 intervals.

    Prerequisites:
        sorting (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "interval_scheduling"

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
        return "select maximum non-overlapping intervals"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an interval scheduling problem.

        Args:
            difficulty: Controls number of intervals.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(4, 5)
        elif difficulty <= 6:
            n = self._rng.randint(5, 7)
        else:
            n = self._rng.randint(7, 9)

        intervals: list[tuple[int, int]] = []
        for _ in range(n):
            s = self._rng.randint(0, 15)
            e = s + self._rng.randint(1, 6)
            intervals.append((s, e))

        sorted_intervals = sorted(intervals, key=lambda x: x[1])
        selected: list[tuple[int, int]] = []
        last_end = -1
        steps = [f"intervals sorted by finish: {sorted_intervals}"]

        for s, e in sorted_intervals:
            if s >= last_end:
                selected.append((s, e))
                last_end = e
                steps.append(f"select [{s},{e}], last_end={last_end}")
            else:
                steps.append(f"skip [{s},{e}] (overlaps)")

        steps.append(f"selected {len(selected)} intervals")

        problem = f"max non-overlapping from {intervals}"
        return problem, {
            "intervals": intervals,
            "sorted": sorted_intervals,
            "selected": selected,
            "count": len(selected),
            "steps": steps,
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
        """Return the selected intervals and count.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"selected: {sd['selected']} ({sd['count']} intervals)"
