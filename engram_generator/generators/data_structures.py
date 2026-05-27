"""Data structure generators.

5 generators across tiers 2-3.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class StackOperationsGenerator(StepGenerator):
    """Simulate a sequence of stack push/pop operations."""

    @property
    def task_name(self) -> str:
        return "stack_operations"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        return "simulate stack"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_ops = min(4 + difficulty * 2, 12)
        ops = []
        stack = []
        pops = []
        for _ in range(n_ops):
            if not stack or self._rng.random() < 0.6:
                val = self._rng.randint(1, 50)
                ops.append(f"push({val})")
                stack.append(val)
            else:
                v = stack.pop()
                ops.append("pop()")
                pops.append(v)
        ops_str = ", ".join(ops)
        return ops_str, {"ops": ops, "stack": stack, "pops": pops}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["ops"]

    def _create_answer(self, sd: dict) -> str:
        top = sd["stack"][-1] if sd["stack"] else "empty"
        return f"top={top}, popped={sd['pops']}"


@register
class QueueOperationsGenerator(StepGenerator):
    """Simulate a sequence of queue enqueue/dequeue operations."""

    @property
    def task_name(self) -> str:
        return "queue_operations"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        return "simulate queue"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_ops = min(4 + difficulty * 2, 12)
        ops = []
        queue = []
        dequeued = []
        for _ in range(n_ops):
            if not queue or self._rng.random() < 0.6:
                val = self._rng.randint(1, 50)
                ops.append(f"enq({val})")
                queue.append(val)
            else:
                v = queue.pop(0)
                ops.append("deq()")
                dequeued.append(v)
        ops_str = ", ".join(ops)
        return ops_str, {"ops": ops, "queue": queue, "dequeued": dequeued}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["ops"]

    def _create_answer(self, sd: dict) -> str:
        front = sd["queue"][0] if sd["queue"] else "empty"
        return f"front={front}, dequeued={sd['dequeued']}"


@register
class BinaryTreeTraversalGenerator(StepGenerator):
    """Produce inorder/preorder/postorder traversal of a binary tree."""

    @property
    def task_name(self) -> str:
        return "binary_tree_traversal"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["stack_operations"]

    def task_description(self, difficulty: int) -> str:
        return "binary tree traversal"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty, 7)
        values = self._rng.sample(range(1, 50), n)
        root = values[0]
        tree = {root: [None, None]}
        nodes = [root]
        for v in values[1:]:
            parent = self._rng.choice(nodes)
            side = 0 if tree[parent][0] is None else (1 if tree[parent][1] is None else -1)
            if side == -1:
                parent = self._rng.choice([p for p in nodes if tree[p][0] is None or tree[p][1] is None])
                side = 0 if tree[parent][0] is None else 1
            tree[parent][side] = v
            tree[v] = [None, None]
            nodes.append(v)

        def inorder(node):
            if node is None: return []
            return inorder(tree[node][0]) + [node] + inorder(tree[node][1])
        def preorder(node):
            if node is None: return []
            return [node] + preorder(tree[node][0]) + preorder(tree[node][1])
        def postorder(node):
            if node is None: return []
            return postorder(tree[node][0]) + postorder(tree[node][1]) + [node]

        mode = self._rng.choice(["inorder", "preorder", "postorder"])
        if mode == "inorder": result = inorder(root)
        elif mode == "preorder": result = preorder(root)
        else: result = postorder(root)

        tree_str = ", ".join(f"{k}:[{tree[k][0]},{tree[k][1]}]" for k in sorted(tree.keys()))
        return (
            f"{mode} of tree root={root}: {tree_str}",
            {"mode": mode, "result": result, "root": root},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"{sd['mode']}: visit {v}" for v in sd["result"]]

    def _create_answer(self, sd: dict) -> str:
        return " ".join(str(v) for v in sd["result"])


@register
class HeapOperationsGenerator(StepGenerator):
    """Simulate insert and extract-min on a min-heap."""

    @property
    def task_name(self) -> str:
        return "heap_operations"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["sorting"]

    def task_description(self, difficulty: int) -> str:
        return "simulate min-heap"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        import heapq
        n_ops = min(4 + difficulty * 2, 10)
        heap = []
        ops = []
        extracted = []
        for _ in range(n_ops):
            if not heap or self._rng.random() < 0.6:
                val = self._rng.randint(1, 100)
                heapq.heappush(heap, val)
                ops.append(f"insert({val})")
            else:
                v = heapq.heappop(heap)
                extracted.append(v)
                ops.append("extract_min()")
        ops_str = ", ".join(ops)
        return ops_str, {"ops": ops, "heap": sorted(heap), "extracted": extracted}

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["ops"]

    def _create_answer(self, sd: dict) -> str:
        top = sd["heap"][0] if sd["heap"] else "empty"
        return f"min={top}, extracted={sd['extracted']}"


@register
class HashTableOpsGenerator(StepGenerator):
    """Simulate hash table insert and lookup."""

    @property
    def task_name(self) -> str:
        return "hash_table_ops"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        return "simulate hash table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        size = min(5 + difficulty, 11)
        n_inserts = min(3 + difficulty, 8)
        table = [None] * size
        ops = []
        for _ in range(n_inserts):
            key = self._rng.randint(1, 100)
            idx = key % size
            ops.append(f"insert({key}) -> slot {idx}")
            if table[idx] is None:
                table[idx] = [key]
            else:
                table[idx].append(key)
        query = self._rng.choice([op.split("(")[1].split(")")[0] for op in ops])
        query = int(query)
        found = any(query in (slot or []) for slot in table)
        return (
            f"size={size}, ops: {'; '.join(ops)}. lookup({query})?",
            {"table": table, "query": query, "found": found, "slot": query % size},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"hash({sd['query']}) = {sd['query']} % {len(sd['table'])} = {sd['slot']}",
                f"check slot {sd['slot']}: {sd['table'][sd['slot']]}"]

    def _create_answer(self, sd: dict) -> str:
        return "FOUND" if sd["found"] else "NOT FOUND"
