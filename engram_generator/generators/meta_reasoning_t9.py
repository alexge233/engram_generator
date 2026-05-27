"""Tier 9 generators — self-directed research and computational reasoning.

Unlocks when Tier 0-8 tasks are mastered. These tasks require the model
to reason about algorithms themselves: design, improve, prove bounds,
diagnose failures, discover invariants, and compare complexity.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class AlgorithmTemplate:
    """Stores a named algorithm with its pseudocode steps and complexity.

    Provides structured access to algorithm descriptions used by
    generators that present, modify, or analyse algorithms.

    Example:
        >>> t = AlgorithmTemplate("find_max", ["scan left to right", "track largest seen"], "O(n)")
        >>> t.name
        'find_max'
        >>> t.complexity
        'O(n)'
    """

    def __init__(self, name: str, steps: list[str], complexity: str) -> None:
        """Initialise an algorithm template.

        Args:
            name: Short identifier for the algorithm.
            steps: Pseudocode steps in execution order.
            complexity: Big-O complexity string.
        """
        self._name = name
        self._steps = steps
        self._complexity = complexity

    @property
    def name(self) -> str:
        """Return the algorithm name."""
        return self._name

    @property
    def steps(self) -> list[str]:
        """Return the pseudocode steps."""
        return self._steps

    @property
    def complexity(self) -> str:
        """Return the complexity string."""
        return self._complexity

    def format_pseudocode(self) -> str:
        """Format steps as numbered pseudocode.

        Returns:
            Multi-line pseudocode string with step numbers.
        """
        numbered = [f"{i + 1}. {s}" for i, s in enumerate(self._steps)]
        return "; ".join(numbered)


class TestCaseRunner:
    """Runs simple algorithms on test inputs for verification.

    Supports a fixed set of algorithmic operations that can be
    executed on small inputs to verify correctness of designed
    or improved algorithms.

    Example:
        >>> r = TestCaseRunner()
        >>> r.find_max([3, 1, 4, 1, 5])
        5
        >>> r.find_median([1, 3, 2])
        2
    """

    def find_max(self, nums: list[int]) -> int:
        """Find the maximum element in a list.

        Args:
            nums: Non-empty list of integers.

        Returns:
            The maximum value.
        """
        result = nums[0]
        for x in nums[1:]:
            if x > result:
                result = x
        return result

    def find_min(self, nums: list[int]) -> int:
        """Find the minimum element in a list.

        Args:
            nums: Non-empty list of integers.

        Returns:
            The minimum value.
        """
        result = nums[0]
        for x in nums[1:]:
            if x < result:
                result = x
        return result

    def find_median(self, nums: list[int]) -> int:
        """Find the median element of a list.

        Args:
            nums: Non-empty list of integers.

        Returns:
            The median value (middle element after sorting).
        """
        sorted_nums = sorted(nums)
        return sorted_nums[len(sorted_nums) // 2]

    def binary_search(self, nums: list[int], target: int) -> int:
        """Perform binary search on a sorted list.

        Args:
            nums: Sorted list of integers.
            target: Value to search for.

        Returns:
            Index of target, or -1 if not found.
        """
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    def count_steps_linear(self, nums: list[int]) -> int:
        """Count comparison steps for a linear scan.

        Args:
            nums: List to scan.

        Returns:
            Number of comparisons (n-1).
        """
        return len(nums) - 1

    def count_steps_binary(self, n: int) -> int:
        """Count worst-case comparison steps for binary search.

        Args:
            n: Size of the sorted array.

        Returns:
            Worst-case number of comparisons (floor(log2(n)) + 1).
        """
        steps = 0
        remaining = n
        while remaining > 0:
            steps += 1
            remaining //= 2
        return steps


@register
class AlgorithmDesignGenerator(StepGenerator):
    """Design an algorithm for a stated computational problem.

    Presents a well-known problem class and asks the model to produce
    a step-by-step algorithm. The target shows pseudocode steps and
    the algorithm is verified by running it on test inputs.

    Input format:
        ``design algorithm to find maximum in a list``

    Target format:
        ``\\text{problem: find maximum in list of N elements} <step>
        1. set max = first element; 2. for each remaining element;
        3. if element > max then max = element; 4. return max <step>
        test: [3,1,4,1,5] -> 5 <step> complexity: O(n) <step> O(n)``

    Difficulty scaling:
        Difficulty 1-2: find max or find min (linear scan).
        Difficulty 3-4: find median or second largest.
        Difficulty 5-6: binary search on sorted array.
        Difficulty 7-8: two-pointer merge or partition.

    Prerequisites:
        method_selection, sorting.

    Example:
        >>> gen = AlgorithmDesignGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'algorithm_design'
    """

    _PROBLEMS = {
        1: ("find_max", "find maximum in list of N elements"),
        2: ("find_min", "find minimum in list of N elements"),
        3: ("find_median", "find median of N elements"),
        4: ("second_largest", "find second largest in list of N elements"),
        5: ("binary_search", "search for target in sorted list"),
        6: ("binary_search", "search for target in sorted list"),
        7: ("merge_sorted", "merge two sorted lists into one"),
        8: ("merge_sorted", "merge two sorted lists into one"),
    }

    _ALGORITHMS: dict[str, AlgorithmTemplate] = {
        "find_max": AlgorithmTemplate(
            "find_max",
            ["set max = first element", "for each remaining element",
             "if element > max then max = element", "return max"],
            "O(n)",
        ),
        "find_min": AlgorithmTemplate(
            "find_min",
            ["set min = first element", "for each remaining element",
             "if element < min then min = element", "return min"],
            "O(n)",
        ),
        "find_median": AlgorithmTemplate(
            "find_median",
            ["sort the list in ascending order",
             "compute middle index = n // 2",
             "return element at middle index"],
            "O(n log n)",
        ),
        "second_largest": AlgorithmTemplate(
            "second_largest",
            ["set max1 = max2 = -infinity",
             "for each element in list",
             "if element > max1 then max2 = max1, max1 = element",
             "else if element > max2 then max2 = element",
             "return max2"],
            "O(n)",
        ),
        "binary_search": AlgorithmTemplate(
            "binary_search",
            ["set lo = 0, hi = n - 1",
             "while lo <= hi",
             "mid = (lo + hi) // 2",
             "if list[mid] == target return mid",
             "if list[mid] < target then lo = mid + 1",
             "else hi = mid - 1",
             "return not found"],
            "O(log n)",
        ),
        "merge_sorted": AlgorithmTemplate(
            "merge_sorted",
            ["set i = 0, j = 0, result = empty",
             "while i < len(A) and j < len(B)",
             "if A[i] <= B[j] then append A[i], i += 1",
             "else append B[j], j += 1",
             "append remaining elements from A or B",
             "return result"],
            "O(n + m)",
        ),
        "count_inversions": AlgorithmTemplate(
            "count_inversions",
            ["modify merge sort to count swaps",
             "during merge, when right element is placed before left",
             "add (len(left) - i) to inversion count",
             "return total inversions"],
            "O(n log n)",
        ),
        "dutch_flag": AlgorithmTemplate(
            "dutch_flag",
            ["three pointers: lo=0, mid=0, hi=n-1",
             "while mid <= hi",
             "if arr[mid]==0: swap(arr[lo],arr[mid]), lo++, mid++",
             "if arr[mid]==1: mid++",
             "if arr[mid]==2: swap(arr[mid],arr[hi]), hi--"],
            "O(n)",
        ),
        "two_sum": AlgorithmTemplate(
            "two_sum",
            ["create hash map",
             "for each element x in array",
             "if (target - x) in hash map, return pair",
             "else add x to hash map"],
            "O(n)",
        ),
        "kadane_max_subarray": AlgorithmTemplate(
            "kadane_max_subarray",
            ["current_sum = 0, max_sum = -infinity",
             "for each element x",
             "current_sum = max(x, current_sum + x)",
             "max_sum = max(max_sum, current_sum)",
             "return max_sum"],
            "O(n)",
        ),
        "topk_quickselect": AlgorithmTemplate(
            "topk_quickselect",
            ["pick random pivot, partition array",
             "if pivot position == k, return left partition",
             "if pivot position < k, recurse on right",
             "else recurse on left"],
            "O(n) average",
        ),
        "flood_fill": AlgorithmTemplate(
            "flood_fill",
            ["start at (r, c) with target colour",
             "if out of bounds or wrong colour, return",
             "set current cell to new colour",
             "recurse on all 4 neighbours"],
            "O(n*m)",
        ),
    }

    _TEST_INPUTS: dict[str, list[int]] = {
        "find_max": [3, 1, 4, 1, 5, 9, 2, 6],
        "find_min": [3, 1, 4, 1, 5, 9, 2, 6],
        "find_median": [7, 2, 9, 4, 5],
        "second_largest": [3, 1, 4, 1, 5, 9, 2, 6],
        "binary_search": [1, 3, 5, 7, 9, 11, 13],
        "merge_sorted": [1, 4, 7, 2, 5, 8],
        "count_inversions": [2, 4, 1, 3, 5],
        "dutch_flag": [0, 2, 1, 0, 2, 1],
        "two_sum": [2, 7, 11, 15],
        "kadane_max_subarray": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
        "topk_quickselect": [3, 2, 1, 5, 6, 4],
        "flood_fill": [1, 1, 0, 1, 1, 1],
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "algorithm_design"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["method_selection", "sorting"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which problem is selected.

        Returns:
            Natural language description.
        """
        _, desc = self._PROBLEMS.get(difficulty, self._PROBLEMS[1])
        return f"design algorithm to {desc}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an algorithm design problem.

        Args:
            difficulty: Controls pool size — higher difficulty unlocks harder algorithms.

        Returns:
            Tuple of (problem_statement, solution_data).
        """
        pool = list(self._PROBLEMS.values())
        if difficulty <= 3:
            pool = pool[:6]
        algo_key, description = self._rng.choice(pool)
        template = self._ALGORITHMS[algo_key]
        test_input = self._TEST_INPUTS.get(algo_key, [1, 2, 3])
        test_result = self._run_test(algo_key, test_input)
        problem = f"\\text{{problem: {description}}}"
        return problem, {
            "algo_key": algo_key, "description": description,
            "template": template, "test_input": test_input,
            "test_result": test_result,
        }

    def _run_test(self, algo_key: str, test_input: list[int]) -> str:
        """Run the algorithm on test input and return the result string.

        Args:
            algo_key: Algorithm identifier.
            test_input: Test data.

        Returns:
            String representation of the result.
        """
        runner = TestCaseRunner()
        if algo_key == "find_max":
            return str(runner.find_max(test_input))
        if algo_key == "find_min":
            return str(runner.find_min(test_input))
        if algo_key == "find_median":
            return str(runner.find_median(test_input))
        if algo_key == "second_largest":
            return str(self._second_largest(test_input))
        if algo_key == "binary_search":
            return str(runner.binary_search(test_input, 7))
        if algo_key == "merge_sorted":
            return str(self._merge_sorted(test_input))
        if algo_key == "count_inversions":
            return str(self._count_inversions(test_input))
        if algo_key == "two_sum":
            return str(self._two_sum(test_input, 9))
        if algo_key == "kadane_max_subarray":
            return str(self._kadane(test_input))
        if algo_key == "dutch_flag":
            return str(sorted(test_input))
        if algo_key == "topk_quickselect":
            return str(sorted(test_input)[:3])
        if algo_key == "flood_fill":
            return "filled region"
        return "result"

    def _second_largest(self, nums: list[int]) -> int:
        """Find the second largest element.

        Args:
            nums: List of integers with at least 2 elements.

        Returns:
            Second largest value.
        """
        sorted_unique = sorted(set(nums), reverse=True)
        return sorted_unique[1] if len(sorted_unique) > 1 else sorted_unique[0]

    def _merge_sorted(self, nums: list[int]) -> str:
        """Merge two halves of a list as if they were sorted sublists.

        Args:
            nums: List split at midpoint into two sorted halves.

        Returns:
            Comma-separated merged result.
        """
        mid = len(nums) // 2
        a = sorted(nums[:mid])
        b = sorted(nums[mid:])
        merged = sorted(a + b)
        return ",".join(str(x) for x in merged)

    def _count_inversions(self, nums: list[int]) -> int:
        """Count pairs (i, j) where i < j but nums[i] > nums[j]."""
        count = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] > nums[j]:
                    count += 1
        return count

    def _two_sum(self, nums: list[int], target: int) -> str:
        """Find two numbers that sum to target."""
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return f"({nums[i]},{nums[j]})"
        return "no pair"

    def _kadane(self, nums: list[int]) -> int:
        """Find maximum subarray sum."""
        cur = best = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            best = max(best, cur)
        return best

    def _create_steps(self, data: dict) -> list[str]:
        """Generate algorithm design steps.

        Args:
            data: Solution data with template and test info.

        Returns:
            Steps showing pseudocode, test verification, and complexity.
        """
        template = data["template"]
        test_str = ",".join(str(x) for x in data["test_input"])
        return [
            template.format_pseudocode(),
            f"test: [{test_str}] -> {data['test_result']}",
            f"complexity: {template.complexity}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the algorithm complexity.

        Args:
            data: Solution data.

        Returns:
            Complexity string.
        """
        return data["template"].complexity


@register
class AlgorithmImprovementGenerator(StepGenerator):
    """Improve a given naive algorithm to a more efficient version.

    Presents an O(n^2) or worse naive solution and asks the model to
    produce a better algorithm. The target shows the improved version
    with its better complexity class.

    Input format:
        ``improve this algorithm``

    Target format:
        ``naive: for each pair check if duplicate -> O(n^2) <step>
        insight: use a set to track seen elements <step>
        improved: for each element, check set membership, add to set
        <step> new complexity: O(n) <step> verify: [1,2,3,2] -> True
        <step> O(n)``

    Difficulty scaling:
        Difficulty 1-2: duplicate detection (O(n^2) -> O(n) via set).
        Difficulty 3-4: max subarray (O(n^2) -> O(n) via Kadane).
        Difficulty 5-6: pair sum (O(n^2) -> O(n) via hash map).
        Difficulty 7-8: closest pair (O(n^2) -> O(n log n) via sort).

    Prerequisites:
        algorithm_design.

    Example:
        >>> gen = AlgorithmImprovementGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'algorithm_improvement'
    """

    _IMPROVEMENTS = {
        1: "duplicate_detection",
        2: "duplicate_detection",
        3: "max_subarray",
        4: "max_subarray",
        5: "pair_sum",
        6: "pair_sum",
        7: "closest_pair",
        8: "closest_pair",
    }

    _NAIVE: dict[str, AlgorithmTemplate] = {
        "duplicate_detection": AlgorithmTemplate(
            "naive_duplicates",
            ["for each element i", "for each element j > i",
             "if list[i] == list[j] return True", "return False"],
            "O(n^2)",
        ),
        "max_subarray": AlgorithmTemplate(
            "naive_max_subarray",
            ["for each start index i", "for each end index j >= i",
             "compute sum of list[i..j]", "track maximum sum"],
            "O(n^2)",
        ),
        "pair_sum": AlgorithmTemplate(
            "naive_pair_sum",
            ["for each element i", "for each element j > i",
             "if list[i] + list[j] == target return (i,j)"],
            "O(n^2)",
        ),
        "closest_pair": AlgorithmTemplate(
            "naive_closest_pair",
            ["for each element i", "for each element j > i",
             "compute |list[i] - list[j]|", "track minimum difference"],
            "O(n^2)",
        ),
    }

    _IMPROVED: dict[str, AlgorithmTemplate] = {
        "duplicate_detection": AlgorithmTemplate(
            "set_duplicates",
            ["create empty set seen", "for each element",
             "if element in seen return True", "add element to seen",
             "return False"],
            "O(n)",
        ),
        "max_subarray": AlgorithmTemplate(
            "kadane",
            ["set current_sum = 0, max_sum = -infinity",
             "for each element",
             "current_sum = max(element, current_sum + element)",
             "max_sum = max(max_sum, current_sum)",
             "return max_sum"],
            "O(n)",
        ),
        "pair_sum": AlgorithmTemplate(
            "hash_pair_sum",
            ["create empty map seen", "for each element",
             "complement = target - element",
             "if complement in seen return (seen[complement], index)",
             "add element:index to seen"],
            "O(n)",
        ),
        "closest_pair": AlgorithmTemplate(
            "sort_closest",
            ["sort the list", "set min_diff = infinity",
             "for each adjacent pair in sorted list",
             "diff = list[i+1] - list[i]",
             "min_diff = min(min_diff, diff)", "return min_diff"],
            "O(n log n)",
        ),
    }

    _INSIGHTS: dict[str, str] = {
        "duplicate_detection": "use a set to track seen elements",
        "max_subarray": "track running sum, reset when negative (Kadane)",
        "pair_sum": "use hash map to find complement in O(1)",
        "closest_pair": "sort first, then only check adjacent pairs",
    }

    _TEST_INPUTS: dict[str, list[int]] = {
        "duplicate_detection": [1, 2, 3, 2, 5],
        "max_subarray": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
        "pair_sum": [2, 7, 11, 15],
        "closest_pair": [4, 1, 7, 3, 9],
    }

    _TEST_RESULTS: dict[str, str] = {
        "duplicate_detection": "True (element 2 repeated)",
        "max_subarray": "6 (subarray [4,-1,2,1])",
        "pair_sum": "(0,1) for target=9",
        "closest_pair": "1 (pair 3,4)",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "algorithm_improvement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["algorithm_design"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which algorithm to improve.

        Returns:
            Natural language description.
        """
        return "improve this algorithm"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an algorithm improvement problem.

        Args:
            difficulty: Controls problem type.

        Returns:
            Tuple of (naive_algorithm_string, solution_data).
        """
        keys = list(self._IMPROVEMENTS.values())
        problem_key = self._rng.choice(keys)
        naive = self._NAIVE[problem_key]
        improved = self._IMPROVED[problem_key]
        insight = self._INSIGHTS[problem_key]
        test_input = self._TEST_INPUTS[problem_key]
        test_result = self._TEST_RESULTS[problem_key]
        problem = f"naive: {naive.format_pseudocode()} -> {naive.complexity}"
        return problem, {
            "problem_key": problem_key, "naive": naive,
            "improved": improved, "insight": insight,
            "test_input": test_input, "test_result": test_result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate improvement reasoning steps.

        Args:
            data: Solution data with naive and improved algorithms.

        Returns:
            Steps showing insight, improved algorithm, and verification.
        """
        improved = data["improved"]
        test_str = ",".join(str(x) for x in data["test_input"])
        return [
            f"insight: {data['insight']}",
            f"improved: {improved.format_pseudocode()}",
            f"new complexity: {improved.complexity}",
            f"verify: [{test_str}] -> {data['test_result']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the improved complexity.

        Args:
            data: Solution data.

        Returns:
            Improved complexity string.
        """
        return data["improved"].complexity


@register
class ImpossibilityProofGenerator(StepGenerator):
    """Prove a lower bound for a computational problem.

    Uses well-known information-theoretic lower bounds and presents
    the argument step by step. The model must identify the counting
    argument that establishes the bound.

    Input format:
        ``prove lower bound for comparison sort``

    Target format:
        ``\\text{lower bound: comparison-based sorting} <step>
        n! possible orderings of n elements <step>
        each comparison eliminates at most half the possibilities <step>
        need at least log2(n!) comparisons <step>
        log2(n!) = Omega(n log n) by Stirling <step> Omega(n log n)``

    Difficulty scaling:
        Difficulty 1-2: searching lower bound Omega(log n).
        Difficulty 3-4: comparison sort Omega(n log n).
        Difficulty 5-6: element uniqueness Omega(n log n).
        Difficulty 7-8: merging lower bound Omega(n).

    Prerequisites:
        algorithm_design, binomial.

    Example:
        >>> gen = ImpossibilityProofGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'impossibility_proof'
    """

    _PROOF_TYPES = {
        1: "searching", 2: "searching",
        3: "comparison_sort", 4: "comparison_sort",
        5: "element_uniqueness", 6: "element_uniqueness",
        7: "merging", 8: "merging",
    }

    _PROBLEMS: dict[str, str] = {
        "searching": "searching in sorted array",
        "comparison_sort": "comparison-based sorting",
        "element_uniqueness": "element uniqueness via comparisons",
        "merging": "merging two sorted lists",
    }

    _BOUNDS: dict[str, str] = {
        "searching": "Omega(log n)",
        "comparison_sort": "Omega(n log n)",
        "element_uniqueness": "Omega(n log n)",
        "merging": "Omega(n)",
    }

    _PROOF_STEPS: dict[str, list[str]] = {
        "searching": [
            "n possible positions for the target",
            "each comparison eliminates at most half the candidates",
            "need at least log2(n) comparisons to distinguish all positions",
            "therefore lower bound is Omega(log n)",
        ],
        "comparison_sort": [
            "n! possible orderings of n elements",
            "each comparison eliminates at most half the possibilities",
            "need at least log2(n!) comparisons",
            "log2(n!) = Omega(n log n) by Stirling approximation",
        ],
        "element_uniqueness": [
            "n! possible orderings if all elements are distinct",
            "algorithm must distinguish distinct set from non-distinct",
            "comparison tree must have at least n! leaves",
            "tree height >= log2(n!) = Omega(n log n)",
        ],
        "merging": [
            "2n elements total from two sorted lists of size n",
            "each comparison determines one element placement",
            "all 2n elements must be placed",
            "at least n comparisons needed in worst case",
        ],
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "impossibility_proof"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["algorithm_design", "binomial"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which lower bound to prove.

        Returns:
            Natural language description.
        """
        proof_type = self._PROOF_TYPES.get(difficulty, "searching")
        problem_name = self._PROBLEMS[proof_type]
        return f"prove lower bound for {problem_name}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a lower bound proof problem.

        Args:
            difficulty: Controls which proof is selected.

        Returns:
            Tuple of (problem_statement, solution_data).
        """
        proof_type = self._rng.choice(list(self._PROBLEMS.keys()))
        problem_name = self._PROBLEMS[proof_type]
        bound = self._BOUNDS[proof_type]
        proof_steps = self._PROOF_STEPS[proof_type]
        problem = f"\\text{{lower bound: {problem_name}}}"
        return problem, {
            "proof_type": proof_type, "problem_name": problem_name,
            "bound": bound, "proof_steps": proof_steps,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate proof steps for the lower bound argument.

        Args:
            data: Solution data with proof steps and bound.

        Returns:
            Steps showing the information-theoretic argument.
        """
        return data["proof_steps"]

    def _create_answer(self, data: dict) -> str:
        """Return the proven lower bound.

        Args:
            data: Solution data.

        Returns:
            Lower bound string.
        """
        return data["bound"]


@register
class FailureAnalysisGenerator(StepGenerator):
    """Identify why an algorithm fails on a specific edge case.

    Presents an algorithm together with a failing input. The model
    must identify the specific edge case that causes failure and
    propose a fix. Covers common pitfalls like integer overflow,
    division by zero, empty collections, and off-by-one errors.

    Input format:
        ``identify why this algorithm fails``

    Target format:
        ``algorithm: binary_search with mid = (lo + hi) / 2;
        input: lo=1000000000, hi=2000000000 <step>
        mid = (1000000000 + 2000000000) / 2 <step>
        3000000000 exceeds 32-bit integer max (2147483647) <step>
        fix: mid = lo + (hi - lo) / 2 <step> integer overflow``

    Difficulty scaling:
        Difficulty 1-2: division by zero in averaging.
        Difficulty 3-4: empty list access without guard.
        Difficulty 5-6: integer overflow in midpoint calculation.
        Difficulty 7-8: off-by-one in boundary conditions.

    Prerequisites:
        error_detection.

    Example:
        >>> gen = FailureAnalysisGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'failure_analysis'
    """

    _FAILURE_TYPES = {
        1: "division_by_zero", 2: "division_by_zero",
        3: "empty_list", 4: "empty_list",
        5: "integer_overflow", 6: "integer_overflow",
        7: "off_by_one", 8: "off_by_one",
    }

    _ALGORITHMS: dict[str, str] = {
        "division_by_zero": "average: return sum(list) / len(list)",
        "empty_list": "find_max: return max(list[0], list[1:]...)",
        "integer_overflow": "binary_search: mid = (lo + hi) / 2",
        "off_by_one": "range_sum: for i in range(lo, hi) sum += arr[i]",
    }

    _FAILING_INPUTS: dict[str, str] = {
        "division_by_zero": "list = []",
        "empty_list": "list = []",
        "integer_overflow": "lo = 1500000000, hi = 2000000000",
        "off_by_one": "arr = [1,2,3,4,5], lo = 0, hi = 5",
    }

    _FAILURE_EXPLANATIONS: dict[str, list[str]] = {
        "division_by_zero": [
            "len([]) = 0",
            "sum([]) / 0 causes division by zero",
            "fix: check if list is empty before dividing",
        ],
        "empty_list": [
            "list has no elements",
            "accessing list[0] raises IndexError",
            "fix: return None or raise ValueError if list is empty",
        ],
        "integer_overflow": [
            "lo + hi = 1500000000 + 2000000000 = 3500000000",
            "3500000000 exceeds 32-bit signed integer max (2147483647)",
            "fix: mid = lo + (hi - lo) / 2 avoids overflow",
        ],
        "off_by_one": [
            "range(0, 5) includes index 4",
            "arr[4] = 5 is the last element",
            "if hi means exclusive end, result is correct",
            "fix: clarify whether hi is inclusive or exclusive",
        ],
    }

    _BUG_NAMES: dict[str, str] = {
        "division_by_zero": "division by zero",
        "empty_list": "empty collection access",
        "integer_overflow": "integer overflow",
        "off_by_one": "off-by-one error",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "failure_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["error_detection"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which failure type is presented.

        Returns:
            Natural language description.
        """
        return "identify why this algorithm fails"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a failure analysis problem.

        Args:
            difficulty: Controls failure type.

        Returns:
            Tuple of (algorithm_with_input, solution_data).
        """
        failure_type = self._rng.choice(list(self._ALGORITHMS.keys()))
        algorithm = self._ALGORITHMS[failure_type]
        failing_input = self._FAILING_INPUTS[failure_type]
        explanation = self._FAILURE_EXPLANATIONS[failure_type]
        bug_name = self._BUG_NAMES[failure_type]
        problem = f"algorithm: {algorithm}; input: {failing_input}"
        return problem, {
            "failure_type": failure_type, "algorithm": algorithm,
            "failing_input": failing_input, "explanation": explanation,
            "bug_name": bug_name,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate failure analysis steps.

        Args:
            data: Solution data with explanation steps.

        Returns:
            Steps showing the trace to the failure and fix.
        """
        return data["explanation"]

    def _create_answer(self, data: dict) -> str:
        """Return the identified bug type.

        Args:
            data: Solution data.

        Returns:
            Bug name string.
        """
        return data["bug_name"]


@register
class InvariantDiscoveryGenerator(StepGenerator):
    """Find a quantity preserved across repeated transformations.

    Applies a transformation multiple times to an initial state and
    asks the model to identify what quantity remains invariant. Covers
    parity invariants, determinant preservation, sum preservation,
    and XOR preservation.

    Input format:
        ``find the invariant``

    Target format:
        ``transformation: swap two elements in list; initial: [3,1,4]
        <step> step 1: swap(0,1) -> [1,3,4], sum=8 <step>
        step 2: swap(1,2) -> [1,4,3], sum=8 <step>
        invariant: sum is preserved (always 8) <step> sum = 8``

    Difficulty scaling:
        Difficulty 1-2: sum preservation under element swaps.
        Difficulty 3-4: XOR preservation under pair-XOR operations.
        Difficulty 5-6: parity preservation under +2/-2 operations.
        Difficulty 7-8: determinant preservation under row operations.

    Prerequisites:
        determinant, generalise_sequence.

    Example:
        >>> gen = InvariantDiscoveryGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'invariant_discovery'
    """

    _INVARIANT_TYPES = {
        1: "sum_swap", 2: "sum_swap",
        3: "xor_pair", 4: "xor_pair",
        5: "parity_shift", 6: "parity_shift",
        7: "determinant_row", 8: "determinant_row",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "invariant_discovery"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["determinant", "generalise_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which invariant type is used.

        Returns:
            Natural language description.
        """
        return "find the invariant"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an invariant discovery problem.

        Args:
            difficulty: Controls invariant type.

        Returns:
            Tuple of (transformation_description, solution_data).
        """
        inv_type = self._INVARIANT_TYPES.get(difficulty, "sum_swap")
        builder = self._get_builder(inv_type)
        return builder(difficulty)

    def _get_builder(self, inv_type: str):
        """Return the builder method for the given invariant type.

        Args:
            inv_type: Invariant type identifier.

        Returns:
            Builder method.
        """
        builders = {
            "sum_swap": self._build_sum_swap,
            "xor_pair": self._build_xor_pair,
            "parity_shift": self._build_parity_shift,
            "determinant_row": self._build_determinant_row,
        }
        return builders[inv_type]

    def _build_sum_swap(self, difficulty: int) -> tuple[str, dict]:
        """Build a sum-preservation-under-swaps problem.

        Args:
            difficulty: Controls list size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        n = 3 + difficulty
        initial = [self._rng.randint(1, 20) for _ in range(n)]
        total = sum(initial)
        steps = self._apply_swaps(initial[:], 3)
        problem = f"transformation: swap two elements; initial: {initial}"
        return problem, {
            "inv_type": "sum", "initial": initial,
            "trace_steps": steps, "invariant_value": str(total),
            "invariant_name": "sum",
        }

    def _apply_swaps(self, state: list[int],
                     num_swaps: int) -> list[dict]:
        """Apply random swaps and record each step.

        Args:
            state: Current list state (modified in place).
            num_swaps: Number of swaps to perform.

        Returns:
            List of step dictionaries with state and invariant value.
        """
        steps: list[dict] = []
        for _ in range(num_swaps):
            i = self._rng.randint(0, len(state) - 1)
            j = self._rng.randint(0, len(state) - 1)
            while j == i:
                j = self._rng.randint(0, len(state) - 1)
            state[i], state[j] = state[j], state[i]
            steps.append({"state": state[:], "value": sum(state)})
        return steps

    def _build_xor_pair(self, difficulty: int) -> tuple[str, dict]:
        """Build an XOR-preservation problem.

        Args:
            difficulty: Controls list size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        n = 3 + difficulty // 2
        initial = [self._rng.randint(1, 15) for _ in range(n)]
        xor_val = initial[0]
        for x in initial[1:]:
            xor_val ^= x
        steps = self._apply_xor_ops(initial[:], 3)
        problem = f"transformation: XOR adjacent pairs; initial: {initial}"
        return problem, {
            "inv_type": "xor", "initial": initial,
            "trace_steps": steps, "invariant_value": str(xor_val),
            "invariant_name": "XOR of all elements",
        }

    def _apply_xor_ops(self, state: list[int],
                       num_ops: int) -> list[dict]:
        """Apply XOR operations on adjacent pairs and record steps.

        Args:
            state: Current list state (modified in place).
            num_ops: Number of operations to perform.

        Returns:
            List of step dictionaries.
        """
        steps: list[dict] = []
        for _ in range(num_ops):
            i = self._rng.randint(0, len(state) - 2)
            state[i] = state[i] ^ state[i + 1]
            xor_val = state[0]
            for x in state[1:]:
                xor_val ^= x
            steps.append({"state": state[:], "value": xor_val})
        return steps

    def _build_parity_shift(self, difficulty: int) -> tuple[str, dict]:
        """Build a parity-preservation problem under even shifts.

        Args:
            difficulty: Controls list size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        n = 3 + difficulty // 2
        initial = [self._rng.randint(1, 20) for _ in range(n)]
        parity = sum(initial) % 2
        steps = self._apply_even_shifts(initial[:], 3)
        problem = f"transformation: add 2 or subtract 2 from elements; initial: {initial}"
        return problem, {
            "inv_type": "parity", "initial": initial,
            "trace_steps": steps, "invariant_value": str(parity),
            "invariant_name": "parity of sum",
        }

    def _apply_even_shifts(self, state: list[int],
                           num_ops: int) -> list[dict]:
        """Apply +2 or -2 to random elements and record steps.

        Args:
            state: Current list state (modified in place).
            num_ops: Number of operations.

        Returns:
            List of step dictionaries.
        """
        steps: list[dict] = []
        for _ in range(num_ops):
            i = self._rng.randint(0, len(state) - 1)
            delta = self._rng.choice([2, -2])
            state[i] += delta
            steps.append({"state": state[:], "value": sum(state) % 2})
        return steps

    def _build_determinant_row(self, difficulty: int) -> tuple[str, dict]:
        """Build a determinant-preservation problem under row addition.

        Args:
            difficulty: Controls matrix values.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        a = self._rng.randint(1, 5)
        b = self._rng.randint(1, 5)
        c = self._rng.randint(1, 5)
        d = self._rng.randint(1, 5)
        det = a * d - b * c
        steps = self._apply_row_additions(a, b, c, d)
        problem = (
            f"transformation: add multiple of one row to another; "
            f"initial: [[{a},{b}],[{c},{d}]]"
        )
        return problem, {
            "inv_type": "determinant", "initial": [[a, b], [c, d]],
            "trace_steps": steps, "invariant_value": str(det),
            "invariant_name": "determinant",
        }

    def _apply_row_additions(self, a: int, b: int,
                             c: int, d: int) -> list[dict]:
        """Apply row operations and record determinant at each step.

        Args:
            a: Matrix element [0][0].
            b: Matrix element [0][1].
            c: Matrix element [1][0].
            d: Matrix element [1][1].

        Returns:
            List of step dictionaries.
        """
        steps: list[dict] = []
        k = self._rng.randint(1, 3)
        new_c = c + k * a
        new_d = d + k * b
        det = a * new_d - b * new_c
        steps.append({"state": [[a, b], [new_c, new_d]], "value": det})
        k2 = self._rng.randint(1, 3)
        new_a = a + k2 * new_c
        new_b = b + k2 * new_d
        det2 = new_a * new_d - new_b * new_c
        steps.append({"state": [[new_a, new_b], [new_c, new_d]], "value": det2})
        return steps

    def _create_steps(self, data: dict) -> list[str]:
        """Generate invariant discovery steps.

        Args:
            data: Solution data with transformation trace.

        Returns:
            Steps showing each transformation and the preserved quantity.
        """
        steps: list[str] = []
        for i, trace in enumerate(data["trace_steps"]):
            steps.append(
                f"step {i + 1}: state={trace['state']}, "
                f"{data['invariant_name']}={trace['value']}"
            )
        steps.append(
            f"invariant: {data['invariant_name']} is preserved "
            f"(always {data['invariant_value']})"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the identified invariant and its value.

        Args:
            data: Solution data.

        Returns:
            Invariant description string.
        """
        return f"{data['invariant_name']} = {data['invariant_value']}"


@register
class ComplexityComparisonGenerator(StepGenerator):
    """Compare two algorithms solving the same problem on a given input.

    Presents two approaches to the same problem with a specific input
    size, and asks which is faster. The model must compute or estimate
    the step count for each algorithm and compare.

    Input format:
        ``which algorithm is faster for this input``

    Target format:
        ``problem: search in sorted list of 1024 elements <step>
        algorithm A: linear scan -> 1024 comparisons <step>
        algorithm B: binary search -> 11 comparisons <step>
        B is faster: 11 < 1024 <step> binary search (11 steps)``

    Difficulty scaling:
        Difficulty 1-2: linear vs binary search (n=16,32).
        Difficulty 3-4: bubble sort vs merge sort (n=8,16).
        Difficulty 5-6: naive multiply vs Karatsuba at threshold.
        Difficulty 7-8: brute force vs dynamic programming.

    Prerequisites:
        algorithm_design.

    Example:
        >>> gen = ComplexityComparisonGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'complexity_comparison'
    """

    _COMPARISON_TYPES = {
        1: "linear_vs_binary", 2: "linear_vs_binary",
        3: "bubble_vs_merge", 4: "bubble_vs_merge",
        5: "naive_vs_karatsuba", 6: "naive_vs_karatsuba",
        7: "brute_vs_dp", 8: "brute_vs_dp",
    }

    _INPUT_SIZES = {
        1: 16, 2: 32, 3: 8, 4: 16, 5: 64, 6: 256, 7: 10, 8: 15,
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "complexity_comparison"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["algorithm_design"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which comparison is presented.

        Returns:
            Natural language description.
        """
        return "which algorithm is faster for this input"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a complexity comparison problem.

        Args:
            difficulty: Controls comparison type and input size.

        Returns:
            Tuple of (problem_description, solution_data).
        """
        comp_type = self._COMPARISON_TYPES.get(difficulty, "linear_vs_binary")
        n = self._INPUT_SIZES.get(difficulty, 16)
        builder = self._get_comparison_builder(comp_type)
        return builder(n)

    def _get_comparison_builder(self, comp_type: str):
        """Return the builder method for the given comparison type.

        Args:
            comp_type: Comparison type identifier.

        Returns:
            Builder method.
        """
        builders = {
            "linear_vs_binary": self._build_linear_vs_binary,
            "bubble_vs_merge": self._build_bubble_vs_merge,
            "naive_vs_karatsuba": self._build_naive_vs_karatsuba,
            "brute_vs_dp": self._build_brute_vs_dp,
        }
        return builders[comp_type]

    def _build_linear_vs_binary(self, n: int) -> tuple[str, dict]:
        """Build a linear search vs binary search comparison.

        Args:
            n: Input size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        linear_steps = n
        binary_steps = self._log2_ceil(n)
        problem = f"problem: search in sorted list of {n} elements"
        return problem, {
            "problem_desc": f"search in sorted list of {n} elements",
            "algo_a": "linear scan", "algo_b": "binary search",
            "steps_a": linear_steps, "steps_b": binary_steps,
            "winner": "binary search", "n": n,
        }

    def _build_bubble_vs_merge(self, n: int) -> tuple[str, dict]:
        """Build a bubble sort vs merge sort comparison.

        Args:
            n: Input size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        bubble_steps = n * (n - 1) // 2
        merge_steps = n * self._log2_ceil(n)
        problem = f"problem: sort {n} elements"
        return problem, {
            "problem_desc": f"sort {n} elements",
            "algo_a": "bubble sort", "algo_b": "merge sort",
            "steps_a": bubble_steps, "steps_b": merge_steps,
            "winner": "merge sort", "n": n,
        }

    def _build_naive_vs_karatsuba(self, n: int) -> tuple[str, dict]:
        """Build a naive multiplication vs Karatsuba comparison.

        Args:
            n: Number of digits.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        naive_steps = n * n
        karatsuba_steps = int(n ** 1.585)
        problem = f"problem: multiply two {n}-digit numbers"
        return problem, {
            "problem_desc": f"multiply two {n}-digit numbers",
            "algo_a": "naive multiplication", "algo_b": "Karatsuba",
            "steps_a": naive_steps, "steps_b": karatsuba_steps,
            "winner": "Karatsuba", "n": n,
        }

    def _build_brute_vs_dp(self, n: int) -> tuple[str, dict]:
        """Build a brute force vs dynamic programming comparison.

        Args:
            n: Problem size (Fibonacci index).

        Returns:
            Tuple of (problem_string, solution_data).
        """
        brute_steps = 2 ** n
        dp_steps = n
        problem = f"problem: compute fibonacci({n})"
        return problem, {
            "problem_desc": f"compute fibonacci({n})",
            "algo_a": "recursive (no memo)", "algo_b": "dynamic programming",
            "steps_a": brute_steps, "steps_b": dp_steps,
            "winner": "dynamic programming", "n": n,
        }

    def _log2_ceil(self, n: int) -> int:
        """Compute ceiling of log base 2.

        Args:
            n: Positive integer.

        Returns:
            Ceiling of log2(n).
        """
        result = 0
        val = 1
        while val < n:
            val *= 2
            result += 1
        return result

    def _create_steps(self, data: dict) -> list[str]:
        """Generate comparison reasoning steps.

        Args:
            data: Solution data with both algorithms and step counts.

        Returns:
            Steps showing each algorithm's cost and the comparison.
        """
        return [
            f"algorithm A: {data['algo_a']} -> {data['steps_a']} steps",
            f"algorithm B: {data['algo_b']} -> {data['steps_b']} steps",
            f"{data['winner']} is faster: {data['steps_b']} < {data['steps_a']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the winning algorithm and its step count.

        Args:
            data: Solution data.

        Returns:
            Winner with step count.
        """
        return f"{data['winner']} ({data['steps_b']} steps)"
