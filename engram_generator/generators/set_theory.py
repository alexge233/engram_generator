"""Set theory generators.

10 generators across tiers 0-2.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class SetMembershipGenerator(StepGenerator):
    """Check if an element is in a set."""

    @property
    def task_name(self) -> str:
        return "set_membership"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return "check set membership"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        size = min(3 + difficulty * 2, 15)
        elements = sorted(self._rng.sample(range(1, size * 3), size))
        query = self._rng.choice(
            elements + [self._rng.randint(1, size * 3)]
        )
        member = query in elements
        s_str = "{" + ", ".join(str(e) for e in elements) + "}"
        return f"is {query} in {s_str}?", {"query": query, "elements": elements, "member": member}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"check {sd['query']} against each element", f"found: {sd['member']}"]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["member"] else "NO"


@register
class SetUnionGenerator(StepGenerator):
    """Compute the union of two sets."""

    @property
    def task_name(self) -> str:
        return "set_union"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return "find union of sets"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty, 10)
        pool = list(range(1, n * 3))
        a = sorted(self._rng.sample(pool, min(n, len(pool))))
        b = sorted(self._rng.sample(pool, min(n, len(pool))))
        union = sorted(set(a) | set(b))
        sa = "{" + ", ".join(str(x) for x in a) + "}"
        sb = "{" + ", ".join(str(x) for x in b) + "}"
        return f"A={sa} B={sb}", {"a": a, "b": b, "union": union}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"combine all elements", f"remove duplicates"]

    def _create_answer(self, sd: dict) -> str:
        return "{" + ", ".join(str(x) for x in sd["union"]) + "}"


@register
class SetIntersectionGenerator(StepGenerator):
    """Compute the intersection of two sets."""

    @property
    def task_name(self) -> str:
        return "set_intersection"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return "find intersection of sets"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty, 10)
        pool = list(range(1, n * 3))
        a = sorted(self._rng.sample(pool, min(n, len(pool))))
        b = sorted(self._rng.sample(pool, min(n, len(pool))))
        inter = sorted(set(a) & set(b))
        sa = "{" + ", ".join(str(x) for x in a) + "}"
        sb = "{" + ", ".join(str(x) for x in b) + "}"
        return f"A={sa} B={sb}", {"a": a, "b": b, "inter": inter}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"find elements in both A and B"]

    def _create_answer(self, sd: dict) -> str:
        if not sd["inter"]:
            return "{}"
        return "{" + ", ".join(str(x) for x in sd["inter"]) + "}"


@register
class SetDifferenceGenerator(StepGenerator):
    """Compute A \\ B (elements in A not in B)."""

    @property
    def task_name(self) -> str:
        return "set_difference"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["set_membership"]

    def task_description(self, difficulty: int) -> str:
        return "find set difference"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty, 10)
        pool = list(range(1, n * 3))
        a = sorted(self._rng.sample(pool, min(n, len(pool))))
        b = sorted(self._rng.sample(pool, min(n, len(pool))))
        diff = sorted(set(a) - set(b))
        sa = "{" + ", ".join(str(x) for x in a) + "}"
        sb = "{" + ", ".join(str(x) for x in b) + "}"
        return f"A={sa} \\\\ B={sb}", {"a": a, "b": b, "diff": diff}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"remove elements of B from A"]

    def _create_answer(self, sd: dict) -> str:
        if not sd["diff"]:
            return "{}"
        return "{" + ", ".join(str(x) for x in sd["diff"]) + "}"


@register
class SetSubsetGenerator(StepGenerator):
    """Check if A is a subset of B."""

    @property
    def task_name(self) -> str:
        return "set_subset"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["set_membership"]

    def task_description(self, difficulty: int) -> str:
        return "check subset relation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty, 8)
        pool = list(range(1, n * 3))
        b = sorted(self._rng.sample(pool, min(n, len(pool))))
        if self._rng.random() < 0.5:
            a = sorted(self._rng.sample(b, min(max(1, n // 2), len(b))))
            is_subset = True
        else:
            a = sorted(self._rng.sample(pool, min(n, len(pool))))
            is_subset = set(a).issubset(set(b))
        sa = "{" + ", ".join(str(x) for x in a) + "}"
        sb = "{" + ", ".join(str(x) for x in b) + "}"
        return f"is {sa} subset of {sb}?", {"a": a, "b": b, "is_subset": is_subset}

    def _create_steps(self, sd: dict) -> list[str]:
        missing = sorted(set(sd["a"]) - set(sd["b"]))
        if missing:
            return [f"{missing} not in B"]
        return [f"all elements of A are in B"]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["is_subset"] else "NO"


@register
class SetCardinalityGenerator(StepGenerator):
    """Compute the cardinality of set operations."""

    @property
    def task_name(self) -> str:
        return "set_cardinality"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["set_union", "set_intersection"]

    def task_description(self, difficulty: int) -> str:
        return "find cardinality"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty, 10)
        pool = list(range(1, n * 3))
        a = sorted(self._rng.sample(pool, min(n, len(pool))))
        b = sorted(self._rng.sample(pool, min(n, len(pool))))
        op = self._rng.choice(["union", "intersection", "difference"])
        if op == "union":
            result = len(set(a) | set(b))
        elif op == "intersection":
            result = len(set(a) & set(b))
        else:
            result = len(set(a) - set(b))
        sa = "{" + ", ".join(str(x) for x in a) + "}"
        sb = "{" + ", ".join(str(x) for x in b) + "}"
        return f"|A {op} B| where A={sa} B={sb}", {"a": a, "b": b, "op": op, "result": result}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"compute {sd['op']}", f"|A|={len(sd['a'])}, |B|={len(sd['b'])}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["result"])


@register
class PowerSetGenerator(StepGenerator):
    """List the power set of a small set."""

    @property
    def task_name(self) -> str:
        return "power_set"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["set_subset"]

    def task_description(self, difficulty: int) -> str:
        return "find power set"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(1 + difficulty, 4)
        elements = sorted(self._rng.sample(range(1, 10), n))
        count = 2 ** n
        s_str = "{" + ", ".join(str(x) for x in elements) + "}"
        return f"P({s_str})", {"elements": elements, "count": count}

    def _create_steps(self, sd: dict) -> list[str]:
        n = len(sd["elements"])
        return [f"|S| = {n}", f"|P(S)| = 2^{n} = {sd['count']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["count"])


@register
class CartesianProductGenerator(StepGenerator):
    """Compute the Cartesian product of two small sets."""

    @property
    def task_name(self) -> str:
        return "cartesian_product"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["set_cardinality"]

    def task_description(self, difficulty: int) -> str:
        return "find Cartesian product size"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        na = min(2 + difficulty, 6)
        nb = min(2 + difficulty, 6)
        a = sorted(self._rng.sample(range(1, 15), na))
        b = sorted(self._rng.sample(range(1, 15), nb))
        count = na * nb
        sa = "{" + ", ".join(str(x) for x in a) + "}"
        sb = "{" + ", ".join(str(x) for x in b) + "}"
        return f"|A × B| where A={sa} B={sb}", {"a": a, "b": b, "count": count}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"|A| = {len(sd['a'])}", f"|B| = {len(sd['b'])}", f"|A × B| = {len(sd['a'])} * {len(sd['b'])}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["count"])


@register
class VennDiagramCountGenerator(StepGenerator):
    """Use inclusion-exclusion to count elements in set unions."""

    @property
    def task_name(self) -> str:
        return "venn_diagram_count"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["set_cardinality"]

    def task_description(self, difficulty: int) -> str:
        return "count using inclusion-exclusion"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a = self._rng.randint(5, 10 * difficulty)
        b = self._rng.randint(5, 10 * difficulty)
        ab = self._rng.randint(0, min(a, b))
        union = a + b - ab
        return (
            f"|A|={a}, |B|={b}, |A ∩ B|={ab}. Find |A ∪ B|",
            {"a": a, "b": b, "ab": ab, "union": union},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"|A ∪ B| = |A| + |B| - |A ∩ B|",
            f"|A ∪ B| = {sd['a']} + {sd['b']} - {sd['ab']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["union"])
