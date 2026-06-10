"""Deep automata and formal language generators.

6 generators across tiers 3-5.
"""

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class DFAComplementGenerator(StepGenerator):
    """Compute the complement of a DFA.

    Swaps accepting and non-accepting states so the complement
    DFA accepts exactly the strings the original rejects.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dfa_complement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dfa_accept"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "complement DFA"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DFA complement problem.

        Args:
            difficulty: Controls state count and input length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_states = min(3 + difficulty // 2, 5)
        accept = set()
        accept.add(self._rng.randint(0, n_states - 1))
        if self._rng.random() < 0.3:
            accept.add(self._rng.randint(0, n_states - 1))
        complement_accept = set(range(n_states)) - accept

        transitions = {}
        for s in range(n_states):
            for sym in "01":
                transitions[(s, sym)] = self._rng.randint(0, n_states - 1)

        length = min(3 + difficulty, 8)
        input_str = "".join(self._rng.choice("01") for _ in range(length))
        state = 0
        trace = [state]
        for sym in input_str:
            state = transitions[(state, sym)]
            trace.append(state)

        orig_accept = state in accept
        comp_accept = state in complement_accept

        trans_str = "; ".join(
            f"(q{s},{sym})->q{transitions[(s, sym)]}"
            for s in range(n_states) for sym in "01"
        )
        problem = (
            f"DFA: q0..q{n_states - 1}, accept={sorted(accept)}, "
            f"{trans_str}. complement on '{input_str}'?"
        )
        return problem, {
            "n_states": n_states, "accept": sorted(accept),
            "complement_accept": sorted(complement_accept),
            "input": input_str, "trace": trace,
            "orig_accept": orig_accept, "comp_accept": comp_accept,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show complement construction and simulation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [
            f"original accept: {sd['accept']}",
            f"complement accept: {sd['complement_accept']}",
        ]
        for i, sym in enumerate(sd["input"]):
            steps.append(f"q{sd['trace'][i]}+'{sym}'->q{sd['trace'][i + 1]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return complement DFA acceptance result.

        Args:
            sd: Solution data dict.

        Returns:
            ACCEPT or REJECT for the complement.
        """
        return f"original={'ACCEPT' if sd['orig_accept'] else 'REJECT'}, complement={'ACCEPT' if sd['comp_accept'] else 'REJECT'}"


@register
class DFAProductGenerator(StepGenerator):
    """Construct the product DFA for intersection of two DFAs.

    States = Q1 x Q2. Transition: (q1,q2) on a goes to
    (delta1(q1,a), delta2(q2,a)). Accept if both components accept.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dfa_product"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dfa_accept"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "product DFA intersection"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a product DFA problem.

        Args:
            difficulty: Controls state counts and input length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n1 = min(2 + difficulty // 3, 3)
        n2 = min(2 + difficulty // 3, 3)
        accept1 = {self._rng.randint(0, n1 - 1)}
        accept2 = {self._rng.randint(0, n2 - 1)}

        trans1 = {}
        trans2 = {}
        for s in range(n1):
            for sym in "01":
                trans1[(s, sym)] = self._rng.randint(0, n1 - 1)
        for s in range(n2):
            for sym in "01":
                trans2[(s, sym)] = self._rng.randint(0, n2 - 1)

        length = min(3 + difficulty, 7)
        input_str = "".join(self._rng.choice("01") for _ in range(length))

        s1, s2 = 0, 0
        trace = [f"({s1},{s2})"]
        for sym in input_str:
            s1 = trans1[(s1, sym)]
            s2 = trans2[(s2, sym)]
            trace.append(f"({s1},{s2})")

        accepted = s1 in accept1 and s2 in accept2
        total_states = n1 * n2

        problem = (
            f"DFA1: {n1} states, accept={sorted(accept1)}. "
            f"DFA2: {n2} states, accept={sorted(accept2)}. "
            f"product on '{input_str}'?"
        )
        return problem, {
            "n1": n1, "n2": n2,
            "accept1": sorted(accept1), "accept2": sorted(accept2),
            "input": input_str, "trace": trace,
            "final": (s1, s2), "accepted": accepted,
            "total_states": total_states,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show product DFA simulation trace.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [f"product states: {sd['n1']}x{sd['n2']}={sd['total_states']}"]
        for i, sym in enumerate(sd["input"]):
            steps.append(f"{sd['trace'][i]}+'{sym}'->{sd['trace'][i + 1]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return whether the product DFA accepts.

        Args:
            sd: Solution data dict.

        Returns:
            ACCEPT or REJECT.
        """
        return "ACCEPT" if sd["accepted"] else "REJECT"


@register
class RegexToDFADirectGenerator(StepGenerator):
    """Construct a DFA directly from a simple regular expression.

    For simple patterns like a*b, (a|b)*, a*ba*, constructs the
    equivalent DFA with explicit states and transitions.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "regex_to_dfa_direct"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["regex_match"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "construct DFA from regex"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a regex-to-DFA problem.

        Args:
            difficulty: Controls regex complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        templates = [
            {
                "regex": "a*b",
                "states": 3,
                "accept": [1],
                "trans": {(0, "a"): 0, (0, "b"): 1, (1, "a"): 2,
                          (1, "b"): 2, (2, "a"): 2, (2, "b"): 2},
                "desc": "any number of a's followed by exactly one b",
            },
            {
                "regex": "(a|b)*",
                "states": 1,
                "accept": [0],
                "trans": {(0, "a"): 0, (0, "b"): 0},
                "desc": "any string of a's and b's including empty",
            },
            {
                "regex": "a*ba*",
                "states": 3,
                "accept": [1],
                "trans": {(0, "a"): 0, (0, "b"): 1, (1, "a"): 1,
                          (1, "b"): 2, (2, "a"): 2, (2, "b"): 2},
                "desc": "exactly one b with any number of a's",
            },
            {
                "regex": "(ab)*",
                "states": 3,
                "accept": [0],
                "trans": {(0, "a"): 1, (0, "b"): 2, (1, "a"): 2,
                          (1, "b"): 0, (2, "a"): 2, (2, "b"): 2},
                "desc": "zero or more repetitions of ab",
            },
            {
                "regex": "a(a|b)*b",
                "states": 3,
                "accept": [2],
                "trans": {(0, "a"): 1, (0, "b"): 3, (1, "a"): 1,
                          (1, "b"): 2, (2, "a"): 1, (2, "b"): 2,
                          (3, "a"): 3, (3, "b"): 3},
                "desc": "starts with a, ends with b, length >= 2",
            },
        ]
        idx = self._rng.randint(0, min(len(templates) - 1, 1 + difficulty))
        tmpl = templates[idx]

        test_len = min(2 + difficulty, 6)
        test_str = "".join(self._rng.choice("ab") for _ in range(test_len))
        state = 0
        trace = [state]
        for sym in test_str:
            key = (state, sym)
            state = tmpl["trans"].get(key, tmpl["states"])
            trace.append(state)
        accepted = state in tmpl["accept"]

        trans_str = "; ".join(
            f"(q{s},{sym})->q{tmpl['trans'][(s, sym)]}"
            for s, sym in sorted(tmpl["trans"].keys())
        )
        problem = (
            f"regex '{tmpl['regex']}' -> DFA. "
            f"test '{test_str}'. transitions: {trans_str}"
        )
        return problem, {
            "regex": tmpl["regex"], "desc": tmpl["desc"],
            "states": tmpl["states"], "accept": tmpl["accept"],
            "test_str": test_str, "trace": trace,
            "accepted": accepted, "trans_str": trans_str,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show DFA construction and test simulation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [
            f"regex: {sd['regex']} ({sd['desc']})",
            f"DFA: {sd['states']} states, accept={sd['accept']}",
        ]
        for i, sym in enumerate(sd["test_str"]):
            steps.append(f"q{sd['trace'][i]}+'{sym}'->q{sd['trace'][i + 1]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return test string acceptance.

        Args:
            sd: Solution data dict.

        Returns:
            ACCEPT or REJECT with state count.
        """
        return f"{'ACCEPT' if sd['accepted'] else 'REJECT'} ({sd['states']} states)"


@register
class LanguageOperationsGenerator(StepGenerator):
    """Perform union, intersection, or concatenation of regular languages.

    Given descriptions of two regular languages, identifies which
    strings belong to the result language under the specified operation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "language_operations"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dfa_accept"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "regular language operations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a language operations problem.

        Args:
            difficulty: Controls test string count and operation.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        langs = [
            ("strings ending in 0", lambda s: len(s) > 0 and s[-1] == "0"),
            ("strings starting with 1", lambda s: len(s) > 0 and s[0] == "1"),
            ("strings with even length", lambda s: len(s) % 2 == 0),
            ("strings containing 11", lambda s: "11" in s),
            ("strings of all 0s", lambda s: len(s) > 0 and all(c == "0" for c in s)),
        ]

        idx1 = self._rng.randint(0, min(len(langs) - 1, 2 + difficulty))
        idx2 = self._rng.randint(0, min(len(langs) - 1, 2 + difficulty))
        while idx2 == idx1:
            idx2 = self._rng.randint(0, len(langs) - 1)

        name1, check1 = langs[idx1]
        name2, check2 = langs[idx2]
        op = self._rng.choice(["union", "intersection"])

        n_tests = min(3 + difficulty, 5)
        tests: list[str] = []
        for _ in range(n_tests):
            length = self._rng.randint(1, min(5, 2 + difficulty))
            tests.append("".join(self._rng.choice("01") for _ in range(length)))

        results: list[tuple[str, bool]] = []
        for t in tests:
            in1 = check1(t)
            in2 = check2(t)
            if op == "union":
                result = in1 or in2
            else:
                result = in1 and in2
            results.append((t, result))

        accepted = [t for t, r in results if r]
        rejected = [t for t, r in results if not r]

        problem = (
            f"L1='{name1}', L2='{name2}'. {op}. "
            f"test: {tests}"
        )
        return problem, {
            "L1": name1, "L2": name2, "op": op,
            "results": results, "accepted": accepted,
            "rejected": rejected,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show membership test for each string.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [f"operation: {sd['op']} of L1 and L2"]
        for t, r in sd["results"]:
            steps.append(f"'{t}': {'in' if r else 'not in'} result")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return accepted and rejected strings.

        Args:
            sd: Solution data dict.

        Returns:
            Lists of accepted and rejected strings.
        """
        return f"accepted={sd['accepted']}, rejected={sd['rejected']}"


@register
class StateEquivalenceGenerator(StepGenerator):
    """Determine state equivalence using the table-filling algorithm.

    Marks pairs of states as distinguishable starting from
    accept/non-accept pairs, then propagates via transitions.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "state_equivalence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dfa_accept"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find equivalent states"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a state equivalence problem.

        Args:
            difficulty: Controls state count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_states = min(3 + difficulty // 2, 5)
        accept = set()
        accept.add(self._rng.randint(0, n_states - 1))
        if self._rng.random() < 0.4:
            accept.add(self._rng.randint(0, n_states - 1))

        transitions = {}
        for s in range(n_states):
            for sym in "01":
                transitions[(s, sym)] = self._rng.randint(0, n_states - 1)

        distinguishable: set[tuple[int, int]] = set()
        for i in range(n_states):
            for j in range(i + 1, n_states):
                if (i in accept) != (j in accept):
                    distinguishable.add((i, j))

        rounds = 0
        changed = True
        while changed:
            changed = False
            rounds += 1
            for i in range(n_states):
                for j in range(i + 1, n_states):
                    if (i, j) in distinguishable:
                        continue
                    for sym in "01":
                        ti = transitions[(i, sym)]
                        tj = transitions[(j, sym)]
                        pair = (min(ti, tj), max(ti, tj))
                        if ti != tj and pair in distinguishable:
                            distinguishable.add((i, j))
                            changed = True
                            break

        equiv_pairs = []
        for i in range(n_states):
            for j in range(i + 1, n_states):
                if (i, j) not in distinguishable:
                    equiv_pairs.append((i, j))

        trans_str = "; ".join(
            f"(q{s},{sym})->q{transitions[(s, sym)]}"
            for s in range(n_states) for sym in "01"
        )
        problem = (
            f"DFA: q0..q{n_states - 1}, accept={sorted(accept)}, "
            f"{trans_str}. equivalent states?"
        )
        return problem, {
            "n_states": n_states, "accept": sorted(accept),
            "distinguishable": sorted(distinguishable),
            "equiv_pairs": equiv_pairs, "rounds": rounds,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show table-filling algorithm steps.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [
            f"initial: mark accept/non-accept pairs",
            f"propagation rounds: {sd['rounds']}",
            f"distinguishable: {sd['distinguishable']}",
        ]
        if sd["equiv_pairs"]:
            steps.append(f"equivalent: {sd['equiv_pairs']}")
        else:
            steps.append("no equivalent pairs")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return equivalent state pairs.

        Args:
            sd: Solution data dict.

        Returns:
            List of equivalent pairs or NONE.
        """
        if sd["equiv_pairs"]:
            return f"equivalent: {sd['equiv_pairs']}"
        return "no equivalent states"


@register
class MyhillNerodeGenerator(StepGenerator):
    """Count Myhill-Nerode equivalence classes for a regular language.

    The number of equivalence classes equals the number of states
    in the minimum DFA for the language.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "myhill_nerode"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dfa_accept"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "count Myhill-Nerode classes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Myhill-Nerode equivalence class counting problem.

        Constructs a DFA, minimizes it, and counts equivalence classes.

        Args:
            difficulty: Controls state count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_states = min(3 + difficulty // 2, 6)
        accept = set()
        accept.add(self._rng.randint(1, n_states - 1))
        if self._rng.random() < 0.3:
            accept.add(self._rng.randint(0, n_states - 1))

        transitions = {}
        for s in range(n_states):
            for sym in "01":
                transitions[(s, sym)] = self._rng.randint(0, n_states - 1)

        distinguishable: set[tuple[int, int]] = set()
        for i in range(n_states):
            for j in range(i + 1, n_states):
                if (i in accept) != (j in accept):
                    distinguishable.add((i, j))

        changed = True
        while changed:
            changed = False
            for i in range(n_states):
                for j in range(i + 1, n_states):
                    if (i, j) in distinguishable:
                        continue
                    for sym in "01":
                        ti = transitions[(i, sym)]
                        tj = transitions[(j, sym)]
                        pair = (min(ti, tj), max(ti, tj))
                        if ti != tj and pair in distinguishable:
                            distinguishable.add((i, j))
                            changed = True
                            break

        parent = list(range(n_states))

        def find(x: int) -> int:
            """Find root of union-find tree.

            Args:
                x: Node to find.

            Returns:
                Root of the component.
            """
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i in range(n_states):
            for j in range(i + 1, n_states):
                if (i, j) not in distinguishable:
                    ri, rj = find(i), find(j)
                    if ri != rj:
                        parent[rj] = ri

        classes: dict[int, list[int]] = {}
        for s in range(n_states):
            root = find(s)
            if root not in classes:
                classes[root] = []
            classes[root].append(s)

        min_states = len(classes)
        trans_str = "; ".join(
            f"(q{s},{sym})->q{transitions[(s, sym)]}"
            for s in range(n_states) for sym in "01"
        )
        problem = (
            f"DFA: q0..q{n_states - 1}, accept={sorted(accept)}, "
            f"{trans_str}. Myhill-Nerode classes?"
        )
        return problem, {
            "n_states": n_states, "accept": sorted(accept),
            "classes": {f"q{k}": [f"q{s}" for s in v]
                        for k, v in classes.items()},
            "min_states": min_states,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show equivalence class construction.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [f"original: {sd['n_states']} states"]
        for rep, members in sd["classes"].items():
            steps.append(f"class [{rep}]: {members}")
        steps.append(f"minimum DFA = {sd['min_states']} states")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the number of equivalence classes.

        Args:
            sd: Solution data dict.

        Returns:
            Equivalence class count.
        """
        return f"{sd['min_states']} equivalence classes"
