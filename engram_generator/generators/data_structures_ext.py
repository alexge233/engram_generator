"""Extended data structure generators.

8 generators across tiers 3-5 covering BST operations, balanced trees,
tries, skip lists, and bloom filters.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _BSTNode:
    """Simple BST node for tree construction.

    Attributes:
        key: Integer key stored in this node.
        left: Left child node or None.
        right: Right child node or None.
    """

    def __init__(self, key: int) -> None:
        self.key = key
        self.left: _BSTNode | None = None
        self.right: _BSTNode | None = None


def _bst_insert_node(root: _BSTNode | None, key: int) -> _BSTNode:
    """Insert a key into a BST and return the root.

    Args:
        root: Current root of the BST.
        key: Key to insert.

    Returns:
        Root of the BST after insertion.
    """
    if root is None:
        return _BSTNode(key)
    if key < root.key:
        root.left = _bst_insert_node(root.left, key)
    else:
        root.right = _bst_insert_node(root.right, key)
    return root


def _bst_inorder(node: _BSTNode | None) -> list[int]:
    """Return inorder traversal of a BST.

    Args:
        node: Root of the subtree.

    Returns:
        List of keys in sorted order.
    """
    if node is None:
        return []
    return _bst_inorder(node.left) + [node.key] + _bst_inorder(node.right)


def _bst_to_str(node: _BSTNode | None) -> str:
    """Compact string representation of a BST.

    Args:
        node: Root of the subtree.

    Returns:
        Parenthesised tree string.
    """
    if node is None:
        return "."
    if node.left is None and node.right is None:
        return str(node.key)
    return f"({_bst_to_str(node.left)} {node.key} {_bst_to_str(node.right)})"


def _bst_height(node: _BSTNode | None) -> int:
    """Return the height of a BST.

    Args:
        node: Root of the subtree.

    Returns:
        Height (0 for a single node, -1 for None).
    """
    if node is None:
        return -1
    return 1 + max(_bst_height(node.left), _bst_height(node.right))


def _bst_min(node: _BSTNode) -> _BSTNode:
    """Return the node with minimum key in the subtree.

    Args:
        node: Root of the subtree.

    Returns:
        Node with smallest key.
    """
    while node.left is not None:
        node = node.left
    return node


def _bst_delete_node(root: _BSTNode | None, key: int) -> _BSTNode | None:
    """Delete a key from a BST and return the new root.

    Args:
        root: Current root.
        key: Key to delete.

    Returns:
        Root after deletion.
    """
    if root is None:
        return None
    if key < root.key:
        root.left = _bst_delete_node(root.left, key)
    elif key > root.key:
        root.right = _bst_delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        successor = _bst_min(root.right)
        root.key = successor.key
        root.right = _bst_delete_node(root.right, successor.key)
    return root


# ---------------------------------------------------------------------------
# 1. BST insert (tier 3)
# ---------------------------------------------------------------------------


@register
class BSTInsertGenerator(StepGenerator):
    """Insert keys into a BST one by one and show the tree after each insertion.

    Difficulty scaling:
        d1-3: 3-4 keys in range 1-20.
        d4-6: 4-5 keys in range 1-50.
        d7-8: 5-6 keys in range 1-80.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bst_insert"

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
            Task description string.
        """
        return "insert keys into BST"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BST insertion sequence.

        Args:
            difficulty: Controls number of keys and value range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(3, 4)
            hi = 20
        elif difficulty <= 6:
            n = self._rng.randint(4, 5)
            hi = 50
        else:
            n = self._rng.randint(5, 6)
            hi = 80
        keys = self._rng.sample(range(1, hi + 1), n)
        root = None
        snapshots = []
        for k in keys:
            root = _bst_insert_node(root, k)
            snapshots.append(f"insert {k}: {_bst_to_str(root)}")
        inorder = _bst_inorder(root)
        return (
            f"Insert keys {keys} into empty BST",
            {"keys": keys, "snapshots": snapshots, "inorder": inorder},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return step-by-step insertion snapshots.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["snapshots"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final inorder traversal.

        Args:
            sd: Solution data.

        Returns:
            Inorder traversal as space-separated string.
        """
        return "inorder: " + " ".join(str(k) for k in sd["inorder"])


# ---------------------------------------------------------------------------
# 2. BST delete (tier 4)
# ---------------------------------------------------------------------------


@register
class BSTDeleteGenerator(StepGenerator):
    """Delete a node from a BST handling leaf, one-child, and two-child cases.

    Difficulty scaling:
        d1-3: 4 keys, delete leaf.
        d4-6: 5 keys, may delete node with one child.
        d7-8: 6 keys, may delete node with two children.

    Prerequisites:
        bst_insert.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bst_delete"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bst_insert"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "delete node from BST"

    def _find_node(self, root: _BSTNode | None,
                   key: int) -> _BSTNode | None:
        """Find a node by key in the BST.

        Args:
            root: Root of the tree.
            key: Key to find.

        Returns:
            The node, or None if not found.
        """
        if root is None:
            return None
        if key == root.key:
            return root
        if key < root.key:
            return self._find_node(root.left, key)
        return self._find_node(root.right, key)

    def _classify_delete(self, node: _BSTNode) -> str:
        """Classify the deletion case for a node.

        Args:
            node: The node to be deleted.

        Returns:
            One of 'leaf', 'one_child', or 'two_children'.
        """
        children = (node.left is not None) + (node.right is not None)
        if children == 0:
            return "leaf"
        if children == 1:
            return "one_child"
        return "two_children"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BST and delete one node.

        Args:
            difficulty: Controls tree size and deletion complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 4
        elif difficulty <= 6:
            n = 5
        else:
            n = 6
        keys = self._rng.sample(range(1, 60), n)
        root = None
        for k in keys:
            root = _bst_insert_node(root, k)
        before = _bst_to_str(root)

        # Choose a target based on difficulty
        all_nodes: list[_BSTNode] = []
        stack = [root]
        while stack:
            nd = stack.pop()
            if nd is not None:
                all_nodes.append(nd)
                stack.extend([nd.left, nd.right])

        if difficulty <= 3:
            # Prefer leaf
            leaves = [nd for nd in all_nodes if nd.left is None and nd.right is None]
            target = self._rng.choice(leaves if leaves else all_nodes)
        elif difficulty <= 6:
            # Prefer one child
            one_child = [nd for nd in all_nodes
                         if (nd.left is None) != (nd.right is None)]
            target = self._rng.choice(one_child if one_child else all_nodes)
        else:
            # Prefer two children
            two_ch = [nd for nd in all_nodes
                      if nd.left is not None and nd.right is not None]
            target = self._rng.choice(two_ch if two_ch else all_nodes)

        del_key = target.key
        case = self._classify_delete(target)
        successor_key = None
        if case == "two_children":
            successor_key = _bst_min(target.right).key

        root = _bst_delete_node(root, del_key)
        after = _bst_to_str(root) if root else "empty"
        after_inorder = _bst_inorder(root) if root else []

        return (
            f"BST: {before}. Delete {del_key}.",
            {
                "before": before, "del_key": del_key,
                "case": case, "successor_key": successor_key,
                "after": after, "inorder": after_inorder,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return deletion steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings describing the deletion procedure.
        """
        steps = [f"find {sd['del_key']} in tree", f"case: {sd['case']}"]
        if sd["case"] == "leaf":
            steps.append(f"remove leaf {sd['del_key']}")
        elif sd["case"] == "one_child":
            steps.append(f"bypass {sd['del_key']} with its child")
        else:
            steps.append(f"replace {sd['del_key']} with successor {sd['successor_key']}")
        steps.append(f"result: {sd['after']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the inorder traversal after deletion.

        Args:
            sd: Solution data.

        Returns:
            Inorder traversal string.
        """
        return "inorder: " + " ".join(str(k) for k in sd["inorder"])


# ---------------------------------------------------------------------------
# 3. AVL rotation (tier 5)
# ---------------------------------------------------------------------------


@register
class AVLRotationGenerator(StepGenerator):
    """After BST insert, compute balance factors and perform AVL rotation.

    Shows the before/after tree and identifies rotation type
    (LL, RR, LR, RL).

    Difficulty scaling:
        d1-4: 4 keys forcing a single rotation.
        d5-8: 5-6 keys, may require double rotation.

    Prerequisites:
        bst_insert.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "avl_rotation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bst_insert"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "identify and perform AVL rotation"

    def _balance_factor(self, node: _BSTNode | None) -> int:
        """Compute the balance factor of a node.

        Args:
            node: BST node.

        Returns:
            Left height minus right height.
        """
        if node is None:
            return 0
        return _bst_height(node.left) - _bst_height(node.right)

    def _rotate_right(self, y: _BSTNode) -> _BSTNode:
        """Perform a right rotation.

        Args:
            y: The unbalanced node.

        Returns:
            New root after rotation.
        """
        x = y.left
        assert x is not None
        y.left = x.right
        x.right = y
        return x

    def _rotate_left(self, x: _BSTNode) -> _BSTNode:
        """Perform a left rotation.

        Args:
            x: The unbalanced node.

        Returns:
            New root after rotation.
        """
        y = x.right
        assert y is not None
        x.right = y.left
        y.left = x
        return y

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BST insertion that causes an AVL violation.

        Args:
            difficulty: Controls tree size and rotation type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Predefined sequences that guarantee specific rotations
        patterns = {
            "LL": [30, 20, 10],
            "RR": [10, 20, 30],
            "LR": [30, 10, 20],
            "RL": [10, 30, 20],
        }
        rot_type = self._rng.choice(["LL", "RR", "LR", "RL"])
        base = patterns[rot_type]
        offset = self._rng.randint(0, 40)
        keys = [k + offset for k in base]

        if difficulty >= 5:
            extra = self._rng.randint(keys[0] + 1, keys[0] + 50)
            while extra in keys:
                extra = self._rng.randint(1, 99)
            keys.append(extra)

        root = None
        for k in keys[:3]:
            root = _bst_insert_node(root, k)
        before = _bst_to_str(root)
        bf = self._balance_factor(root)

        # Perform the fix
        if rot_type == "LL":
            root = self._rotate_right(root)
        elif rot_type == "RR":
            root = self._rotate_left(root)
        elif rot_type == "LR":
            root.left = self._rotate_left(root.left)
            root = self._rotate_right(root)
        else:  # RL
            root.right = self._rotate_right(root.right)
            root = self._rotate_left(root)

        after = _bst_to_str(root)
        return (
            f"Insert {keys[:3]} into AVL tree",
            {
                "keys": keys[:3], "before": before, "bf": bf,
                "rot_type": rot_type, "after": after,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return rotation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return [
            f"BST after inserts: {sd['before']}",
            f"balance factor at root: {sd['bf']}",
            f"|BF|>1, rotation type: {sd['rot_type']}",
            f"after rotation: {sd['after']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return rotation type and final tree.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"{sd['rot_type']} rotation, tree: {sd['after']}"


# ---------------------------------------------------------------------------
# 4. Red-black tree insert (tier 5)
# ---------------------------------------------------------------------------


@register
class RedBlackInsertGenerator(StepGenerator):
    """Insert into a red-black tree and fix violations by recoloring or rotating.

    Simplified for small trees (3-5 nodes). Shows color assignments.

    Difficulty scaling:
        d1-4: 3 nodes.
        d5-8: 4-5 nodes.

    Prerequisites:
        bst_insert.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "red_black_insert"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bst_insert"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "insert into red-black tree"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an RB tree insertion with violation fix.

        Args:
            difficulty: Controls number of keys.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 3 if difficulty <= 4 else self._rng.randint(4, 5)
        keys = self._rng.sample(range(1, 50), n)
        # Simulate simplified RB insert
        colors: dict[int, str] = {}
        root_key = keys[0]
        colors[root_key] = "B"
        steps_log = [f"insert {root_key}: root, color B"]

        root = _BSTNode(root_key)
        for k in keys[1:]:
            root = _bst_insert_node(root, k)
            colors[k] = "R"
            step_desc = f"insert {k}: color R"

            # Check parent color (simplified)
            parent_key = self._find_parent_key(root, k)
            if parent_key is not None and colors.get(parent_key) == "R":
                # Fix: recolor parent and grandparent
                gp_key = self._find_parent_key(root, parent_key)
                colors[parent_key] = "B"
                step_desc += f", parent {parent_key} red -> recolor B"
                if gp_key is not None and gp_key != root_key:
                    colors[gp_key] = "R"
                    step_desc += f", grandparent {gp_key} -> R"
            steps_log.append(step_desc)

        # Root is always black
        colors[root_key] = "B"
        color_str = ", ".join(f"{k}:{colors[k]}" for k in keys)
        return (
            f"RB-insert keys {keys}",
            {"keys": keys, "steps_log": steps_log, "colors": color_str},
        )

    def _find_parent_key(self, root: _BSTNode | None,
                         key: int) -> int | None:
        """Find the parent of a node in the BST.

        Args:
            root: Root of the tree.
            key: Key whose parent to find.

        Returns:
            Parent key or None if key is root.
        """
        if root is None or root.key == key:
            return None
        stack: list[tuple[_BSTNode, _BSTNode | None]] = [(root, None)]
        while stack:
            node, parent = stack.pop()
            if node.key == key:
                return parent.key if parent else None
            if node.left is not None:
                stack.append((node.left, node))
            if node.right is not None:
                stack.append((node.right, node))
        return None

    def _create_steps(self, sd: dict) -> list[str]:
        """Return insertion and fix steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return final color assignments.

        Args:
            sd: Solution data.

        Returns:
            Color assignment string.
        """
        return sd["colors"]


# ---------------------------------------------------------------------------
# 5. B-tree insert (tier 5)
# ---------------------------------------------------------------------------


@register
class BTreeInsertGenerator(StepGenerator):
    """Insert into a B-tree of order 3 (2-3 tree) and split full nodes.

    Difficulty scaling:
        d1-4: 4 keys.
        d5-8: 5-6 keys, more splits.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "b_tree_insert"

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
            Task description string.
        """
        return "insert into B-tree (order 3)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate B-tree insertions with node splitting.

        Args:
            difficulty: Controls number of keys.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 4 if difficulty <= 4 else self._rng.randint(5, 6)
        keys = self._rng.sample(range(1, 40), n)
        max_keys = 2  # order 3 -> max 2 keys per node
        # Simulate with a flat representation: list of sorted node lists
        nodes: list[list[int]] = [[]]
        steps_log = []
        for k in keys:
            # Find target node (simplified: single level until split)
            idx = 0
            for i, node in enumerate(nodes):
                if not node or k < node[0]:
                    idx = i
                    break
                idx = i
            nodes[idx].append(k)
            nodes[idx].sort()
            step = f"insert {k} -> node {nodes[idx]}"

            if len(nodes[idx]) > max_keys:
                # Split: middle goes up, create two children
                mid = nodes[idx][1]
                left_part = [nodes[idx][0]]
                right_part = [nodes[idx][2]] if len(nodes[idx]) > 2 else []
                nodes[idx] = left_part
                if right_part:
                    nodes.insert(idx + 1, right_part)
                step += f", split: promote {mid}"
            steps_log.append(step)

        final = " | ".join(str(nd) for nd in nodes)
        return (
            f"B-tree order 3, insert {keys}",
            {"keys": keys, "steps_log": steps_log, "final": final},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return insertion and split steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final B-tree nodes.

        Args:
            sd: Solution data.

        Returns:
            Final node representation.
        """
        return sd["final"]


# ---------------------------------------------------------------------------
# 6. Trie operations (tier 4)
# ---------------------------------------------------------------------------


@register
class TrieOperationsGenerator(StepGenerator):
    """Insert words into a trie, search for prefixes, and count matches.

    Difficulty scaling:
        d1-3: 3 short words, search one prefix.
        d4-6: 4 words, search two prefixes.
        d7-8: 5 words, search two prefixes.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "trie_operations"

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
            Task description string.
        """
        return "trie insert and prefix search"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate trie operations with prefix queries.

        Args:
            difficulty: Controls number of words and queries.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        word_pool = [
            "cat", "car", "card", "care", "can",
            "bat", "bar", "ban", "bad",
            "dog", "dot", "do", "den",
            "tea", "ten", "top", "tap",
        ]
        if difficulty <= 3:
            n_words = 3
        elif difficulty <= 6:
            n_words = 4
        else:
            n_words = 5
        words = self._rng.sample(word_pool, n_words)

        # Build trie as nested dict
        trie: dict = {}
        for w in words:
            node = trie
            for ch in w:
                if ch not in node:
                    node[ch] = {}
                node = node[ch]
            node["$"] = True

        # Pick prefix queries
        prefix = words[0][:2]
        matches = [w for w in words if w.startswith(prefix)]

        steps = [f"insert '{w}'" for w in words]
        steps.append(f"search prefix '{prefix}'")
        steps.append(f"matches: {matches}")

        return (
            f"Trie: insert {words}, prefix search '{prefix}'",
            {"words": words, "prefix": prefix,
             "matches": matches, "steps": steps},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return trie operation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the count and list of prefix matches.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"count={len(sd['matches'])}, words={sd['matches']}"


# ---------------------------------------------------------------------------
# 7. Skip list (tier 5)
# ---------------------------------------------------------------------------


@register
class SkipListGenerator(StepGenerator):
    """Insert into a skip list with coin flips determining level, then search.

    Difficulty scaling:
        d1-4: 4 elements, max level 2.
        d5-8: 5-6 elements, max level 3.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "skip_list"

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
            Task description string.
        """
        return "insert into skip list and search"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate skip list insertions and a search query.

        Args:
            difficulty: Controls number of elements and max level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n = 4
            max_level = 2
        else:
            n = self._rng.randint(5, 6)
            max_level = 3
        keys = self._rng.sample(range(1, 50), n)

        # Build skip list levels
        levels: dict[int, int] = {}  # key -> level (0-based)
        steps_log = []
        for k in keys:
            lvl = 0
            while lvl < max_level - 1 and self._rng.random() < 0.5:
                lvl += 1
            levels[k] = lvl
            steps_log.append(f"insert {k}: level {lvl}")

        # Search for a key
        search_key = self._rng.choice(keys)
        sorted_keys = sorted(keys)
        search_path = []
        for lv in range(max_level - 1, -1, -1):
            keys_at_level = sorted([k for k, v in levels.items() if v >= lv])
            for kk in keys_at_level:
                if kk <= search_key:
                    search_path.append(f"L{lv}:{kk}")
                    if kk == search_key:
                        break
        steps_log.append(f"search {search_key}: {' -> '.join(search_path)}")

        return (
            f"Skip list insert {keys}, search {search_key}",
            {"keys": keys, "levels": levels, "search_key": search_key,
             "search_path": search_path, "steps_log": steps_log},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return skip list operation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return search result.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"found {sd['search_key']} via {' -> '.join(sd['search_path'])}"


# ---------------------------------------------------------------------------
# 8. Bloom filter (tier 4)
# ---------------------------------------------------------------------------


@register
class BloomFilterGenerator(StepGenerator):
    """Insert items using k hash functions and query membership.

    If all k bits set, answer is 'maybe'. If any bit is 0, 'definitely not'.
    Computes false positive rate.

    Difficulty scaling:
        d1-3: m=8 bits, k=2 hashes, 3 inserts.
        d4-6: m=12 bits, k=3 hashes, 4 inserts.
        d7-8: m=16 bits, k=3 hashes, 5 inserts.

    Prerequisites:
        modular.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bloom_filter"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "bloom filter insert and query"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate bloom filter insertions and a query.

        Args:
            difficulty: Controls filter size and hash count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            m, k, n_insert = 8, 2, 3
        elif difficulty <= 6:
            m, k, n_insert = 12, 3, 4
        else:
            m, k, n_insert = 16, 3, 5

        items = self._rng.sample(range(1, 100), n_insert + 1)
        insert_items = items[:n_insert]
        query_item = self._rng.choice(
            [items[-1], self._rng.choice(insert_items)]
        )

        # Hash functions: h_i(x) = (x * (i+1) + i*7) % m
        bits = [0] * m
        steps_log = []
        for item in insert_items:
            positions = []
            for i in range(k):
                pos = (item * (i + 1) + i * 7) % m
                bits[pos] = 1
                positions.append(pos)
            steps_log.append(f"insert {item}: bits {positions}")

        # Query
        query_positions = []
        all_set = True
        for i in range(k):
            pos = (query_item * (i + 1) + i * 7) % m
            query_positions.append(pos)
            if bits[pos] == 0:
                all_set = False
        result = "maybe" if all_set else "definitely not"

        # False positive rate: (1 - (1 - 1/m)^(kn))^k
        n = n_insert
        fp_rate = (1 - (1 - 1 / m) ** (k * n)) ** k
        fp_rate = round(fp_rate, 4)

        steps_log.append(f"query {query_item}: check bits {query_positions}")
        steps_log.append(f"bits state: {''.join(str(b) for b in bits)}")

        return (
            f"Bloom filter m={m}, k={k}. Insert {insert_items}. Query {query_item}?",
            {
                "m": m, "k": k, "insert_items": insert_items,
                "query_item": query_item, "result": result,
                "fp_rate": fp_rate, "steps_log": steps_log,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Return bloom filter operation steps.

        Args:
            sd: Solution data.

        Returns:
            Step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Return query result and false positive rate.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"{sd['result']}, FP rate={sd['fp_rate']}"
