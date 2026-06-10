"""Formal language theory generators.

8 generators across tiers 5-6 covering NFA-to-DFA conversion,
regex-to-NFA construction, context-free grammars, pushdown automata,
pumping lemma proofs, Chomsky normal form, and Chomsky hierarchy
classification.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _NFASpec:
    """A small NFA specification for generation helpers.

    Stores states, alphabet, transition map, start state, and accept states.
    Transitions map (state, symbol) to a set of target states.

    Attributes:
        states: Set of state names.
        alphabet: Set of input symbols.
        transitions: Mapping from (state, symbol) to set of next states.
        start: Start state name.
        accept: Set of accepting state names.
    """

    def __init__(self, states: set[str], alphabet: set[str],
                 transitions: dict[tuple[str, str], set[str]],
                 start: str, accept: set[str]) -> None:
        """Initialise the NFA specification.

        Args:
            states: All state names.
            alphabet: Input symbol set.
            transitions: NFA transition function.
            start: Start state.
            accept: Accepting states.
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start = start
        self.accept = accept

    def format_transitions(self) -> str:
        """Format the transition table as a compact string.

        Returns:
            Semicolon-separated transition entries.
        """
        parts = []
        for (s, sym), targets in sorted(self.transitions.items()):
            if targets:
                parts.append(f"d({s},{sym})={{{','.join(sorted(targets))}}}")
        return "; ".join(parts)


class _GrammarSpec:
    """A context-free grammar specification.

    Stores productions as a dict mapping nonterminals to lists of
    right-hand side strings.

    Attributes:
        start: Start symbol.
        productions: Mapping from nonterminal to list of RHS strings.
    """

    def __init__(self, start: str,
                 productions: dict[str, list[str]]) -> None:
        """Initialise the grammar.

        Args:
            start: Start nonterminal.
            productions: Production rules.
        """
        self.start = start
        self.productions = productions

    def format_rules(self) -> str:
        """Format grammar rules as a compact string.

        Returns:
            Rules separated by semicolons with alternatives using |.
        """
        parts = []
        for nt in sorted(self.productions):
            rhs = " | ".join(self.productions[nt])
            parts.append(f"{nt} -> {rhs}")
        return "; ".join(parts)


# ---------------------------------------------------------------------------
# 1. NFA to DFA (tier 5)
# ---------------------------------------------------------------------------

@register
class NFAToDFAGenerator(StepGenerator):
    """Convert a small NFA to an equivalent DFA via subset construction.

    Generates NFAs with 2-4 states over alphabet {a,b}, then performs
    the subset construction algorithm. Shows the reachable state subsets
    and the resulting DFA transition table.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nfa_to_dfa"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["nfa_simulate"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "convert NFA to DFA via subset construction"

    def _build_nfa(self, difficulty: int) -> _NFASpec:
        """Build a random small NFA.

        Args:
            difficulty: Controls the number of states (2-4).

        Returns:
            An NFA specification.
        """
        n_states = min(2 + difficulty // 3, 4)
        state_names = [f"q{i}" for i in range(n_states)]
        alphabet = {"a", "b"}
        transitions: dict[tuple[str, str], set[str]] = {}
        for s in state_names:
            for sym in sorted(alphabet):
                n_targets = self._rng.randint(0, min(2, n_states))
                targets = set(self._rng.sample(state_names, n_targets))
                transitions[(s, sym)] = targets
        n_accept = self._rng.randint(1, max(1, n_states // 2))
        accept = set(self._rng.sample(state_names[1:], min(n_accept, n_states - 1)))
        if not accept:
            accept = {state_names[-1]}
        return _NFASpec(set(state_names), alphabet, transitions, "q0", accept)

    def _subset_construction(self, nfa: _NFASpec) -> dict:
        """Run subset construction on the NFA.

        Args:
            nfa: The source NFA.

        Returns:
            Dict with dfa_transitions, dfa_accept, reachable subsets, and steps.
        """
        alphabet = sorted(nfa.alphabet)
        start_set = frozenset({nfa.start})
        queue = [start_set]
        visited: set[frozenset[str]] = {start_set}
        dfa_trans: dict[tuple[str, str], str] = {}
        steps: list[str] = []

        def subset_label(ss: frozenset[str]) -> str:
            return "{" + ",".join(sorted(ss)) + "}" if ss else "{}"

        while queue:
            current = queue.pop(0)
            for sym in alphabet:
                nxt: set[str] = set()
                for s in current:
                    nxt |= nfa.transitions.get((s, sym), set())
                nxt_frozen = frozenset(nxt)
                label_from = subset_label(current)
                label_to = subset_label(nxt_frozen)
                dfa_trans[(label_from, sym)] = label_to
                steps.append(f"d'({label_from},{sym}) = {label_to}")
                if nxt_frozen not in visited:
                    visited.add(nxt_frozen)
                    queue.append(nxt_frozen)

        dfa_accept = []
        for ss in visited:
            if ss & nfa.accept:
                dfa_accept.append(subset_label(ss))

        return {
            "dfa_transitions": dfa_trans,
            "dfa_accept": sorted(dfa_accept),
            "reachable": sorted(subset_label(ss) for ss in visited),
            "steps": steps,
        }

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an NFA-to-DFA conversion problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        nfa = self._build_nfa(difficulty)
        result = self._subset_construction(nfa)
        problem = (
            f"NFA: states={{{','.join(sorted(nfa.states))}}}, "
            f"accept={{{','.join(sorted(nfa.accept))}}}, "
            f"start={nfa.start}; {nfa.format_transitions()}"
        )
        result["nfa"] = nfa
        return problem, result

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate solution steps showing subset construction.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Extract the DFA description as the final answer.

        Args:
            solution_data: All computed solution information.

        Returns:
            DFA states and accept states.
        """
        return (
            f"DFA states: {solution_data['reachable']}; "
            f"accept: {solution_data['dfa_accept']}"
        )


# ---------------------------------------------------------------------------
# 2. Regex to NFA (tier 5)
# ---------------------------------------------------------------------------

@register
class RegexToNFAGenerator(StepGenerator):
    """Convert a simple regular expression to an NFA via Thompson's construction.

    Supports operators: concatenation, union (|), and Kleene star (*).
    Produces an NFA transition list using small state numbers.
    """

    _TEMPLATES: list[dict] = [
        {"regex": "a|b", "desc": "union of a and b"},
        {"regex": "ab", "desc": "concatenation a then b"},
        {"regex": "a*", "desc": "Kleene star of a"},
        {"regex": "(a|b)*", "desc": "Kleene star of union a|b"},
        {"regex": "a*b", "desc": "zero or more a then b"},
        {"regex": "ab*", "desc": "a then zero or more b"},
        {"regex": "(ab)*", "desc": "Kleene star of ab"},
        {"regex": "a|b*", "desc": "a or Kleene star of b"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "regex_to_nfa"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["regex_match"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "convert regex to NFA (Thompson's construction)"

    def _thompson_union(self, label: str, sym_a: str, sym_b: str,
                        base: int) -> tuple[list[str], list[str], int, int]:
        """Build Thompson NFA fragment for union.

        Args:
            label: Description label.
            sym_a: First alternative symbol.
            sym_b: Second alternative symbol.
            base: Starting state number.

        Returns:
            Tuple of (transitions, steps, start_state, accept_state).
        """
        s = base
        a1, a2 = base + 1, base + 2
        b1, b2 = base + 3, base + 4
        f = base + 5
        trans = [
            f"({s},eps)->{a1}", f"({s},eps)->{b1}",
            f"({a1},{sym_a})->{a2}", f"({b1},{sym_b})->{b2}",
            f"({a2},eps)->{f}", f"({b2},eps)->{f}",
        ]
        steps = [
            f"new start {s} with eps to {a1},{b1}",
            f"{a1} --{sym_a}--> {a2}",
            f"{b1} --{sym_b}--> {b2}",
            f"{a2},{b2} eps to accept {f}",
        ]
        return trans, steps, s, f

    def _thompson_concat(self, sym_a: str, sym_b: str,
                         base: int) -> tuple[list[str], list[str], int, int]:
        """Build Thompson NFA fragment for concatenation.

        Args:
            sym_a: First symbol.
            sym_b: Second symbol.
            base: Starting state number.

        Returns:
            Tuple of (transitions, steps, start_state, accept_state).
        """
        s = base
        m = base + 1
        f = base + 2
        trans = [f"({s},{sym_a})->{m}", f"({m},{sym_b})->{f}"]
        steps = [f"{s} --{sym_a}--> {m}", f"{m} --{sym_b}--> {f}"]
        return trans, steps, s, f

    def _thompson_star(self, sym: str,
                       base: int) -> tuple[list[str], list[str], int, int]:
        """Build Thompson NFA fragment for Kleene star.

        Args:
            sym: Symbol to repeat.
            base: Starting state number.

        Returns:
            Tuple of (transitions, steps, start_state, accept_state).
        """
        s = base
        inner_s, inner_f = base + 1, base + 2
        f = base + 3
        trans = [
            f"({s},eps)->{inner_s}", f"({s},eps)->{f}",
            f"({inner_s},{sym})->{inner_f}",
            f"({inner_f},eps)->{inner_s}", f"({inner_f},eps)->{f}",
        ]
        steps = [
            f"new start {s}, eps to {inner_s} and accept {f}",
            f"{inner_s} --{sym}--> {inner_f}",
            f"{inner_f} eps back to {inner_s} and to accept {f}",
        ]
        return trans, steps, s, f

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a regex-to-NFA conversion problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        template = self._TEMPLATES[idx]
        regex = template["regex"]
        base = 0

        if regex == "a|b":
            trans, steps, s, f = self._thompson_union("union", "a", "b", base)
        elif regex == "ab":
            trans, steps, s, f = self._thompson_concat("a", "b", base)
        elif regex == "a*":
            trans, steps, s, f = self._thompson_star("a", base)
        elif regex == "(a|b)*":
            u_trans, u_steps, u_s, u_f = self._thompson_union(
                "inner union", "a", "b", base + 1
            )
            s = base
            f = u_f + 1
            trans = [
                f"({s},eps)->{u_s}", f"({s},eps)->{f}",
            ] + u_trans + [
                f"({u_f},eps)->{u_s})", f"({u_f},eps)->{f}",
            ]
            steps = [
                f"star wrapper: start {s}, eps to {u_s} and {f}",
            ] + u_steps + [
                f"{u_f} eps back to {u_s} and to accept {f}",
            ]
        elif regex == "a*b":
            star_trans, star_steps, ss, sf = self._thompson_star("a", base)
            mid = sf
            f = sf + 1
            trans = star_trans + [f"({mid},{b})->{f}" for b in ["b"]]
            steps = star_steps + [f"concat: {mid} --b--> {f}"]
            s = ss
        elif regex == "ab*":
            s = base
            mid = base + 1
            star_trans, star_steps, ss2, sf = self._thompson_star("b", mid)
            trans = [f"({s},a)->{mid}"] + star_trans
            steps = [f"{s} --a--> {mid}"] + star_steps
            f = sf
        elif regex == "(ab)*":
            s = base
            inner_s, inner_m, inner_f = base + 1, base + 2, base + 3
            f = base + 4
            trans = [
                f"({s},eps)->{inner_s}", f"({s},eps)->{f}",
                f"({inner_s},a)->{inner_m}", f"({inner_m},b)->{inner_f}",
                f"({inner_f},eps)->{inner_s}", f"({inner_f},eps)->{f}",
            ]
            steps = [
                f"star start {s}, eps to {inner_s} and {f}",
                f"{inner_s} --a--> {inner_m} --b--> {inner_f}",
                f"{inner_f} eps back to {inner_s} and to accept {f}",
            ]
        else:  # "a|b*"
            s = base
            a1, a2 = base + 1, base + 2
            star_trans, star_steps, ss2, sf = self._thompson_star("b", base + 3)
            f = sf + 1
            trans = [
                f"({s},eps)->{a1}", f"({s},eps)->{ss2}",
                f"({a1},a)->{a2}", f"({a2},eps)->{f}",
            ] + star_trans + [f"({sf},eps)->{f}"]
            steps = [
                f"union start {s}, eps to {a1} and {ss2}",
                f"{a1} --a--> {a2}, eps to accept {f}",
            ] + star_steps + [f"{sf} eps to accept {f}"]

        problem = f"regex: {regex}"
        return problem, {
            "regex": regex,
            "transitions": trans,
            "steps": steps,
            "start": s,
            "accept": f,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate solution steps for Thompson's construction.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Extract the NFA transitions as the final answer.

        Args:
            solution_data: All computed solution information.

        Returns:
            NFA transition list with start and accept states.
        """
        trans_str = ", ".join(solution_data["transitions"])
        return (
            f"start={solution_data['start']}, "
            f"accept={solution_data['accept']}, "
            f"transitions: {trans_str}"
        )


# ---------------------------------------------------------------------------
# 3. CFG Derivation (tier 5)
# ---------------------------------------------------------------------------

@register
class CFGDerivationGenerator(StepGenerator):
    """Derive a string from a context-free grammar using leftmost derivation.

    Uses grammars like S -> aSb | ab, S -> aS | a, etc. to produce
    derivation sequences showing how a target string is generated.
    """

    _GRAMMARS: list[dict] = [
        {
            "rules": {"S": ["aSb", "ab"]},
            "family": "a^n b^n",
        },
        {
            "rules": {"S": ["aSa", "bSb", "a", "b", ""]},
            "family": "palindromes",
        },
        {
            "rules": {"S": ["SS", "(S)", "()"]},
            "family": "balanced parens",
        },
        {
            "rules": {"S": ["aB", "bA"], "A": ["aS", "bAA", "a"],
                      "B": ["bS", "aBB", "b"]},
            "family": "equal a,b count",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cfg_derivation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["regex_match"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "show leftmost derivation in context-free grammar"

    def _derive_anbn(self, depth: int) -> tuple[str, list[str]]:
        """Derive a^n b^n string with leftmost derivation steps.

        Args:
            depth: Nesting depth (number of a's and b's).

        Returns:
            Tuple of (target_string, derivation_steps).
        """
        if depth <= 1:
            return "ab", ["S => ab"]
        steps = []
        current = "S"
        for i in range(depth - 1):
            new = current.replace("S", "aSb", 1)
            steps.append(f"{current} => {new}")
            current = new
        final = current.replace("S", "ab", 1)
        steps.append(f"{current} => {final}")
        return final, steps

    def _derive_palindrome(self, rng_ref, depth: int) -> tuple[str, list[str]]:
        """Derive a palindrome with leftmost derivation steps.

        Args:
            rng_ref: Random generator for symbol choices.
            depth: Controls palindrome length.

        Returns:
            Tuple of (target_string, derivation_steps).
        """
        steps = []
        current = "S"
        for _ in range(min(depth, 3)):
            wrap = rng_ref.choice(["aSa", "bSb"])
            new = current.replace("S", wrap, 1)
            steps.append(f"{current} => {new}")
            current = new
        base = rng_ref.choice(["a", "b", ""])
        final = current.replace("S", base, 1)
        steps.append(f"{current} => {final}")
        return final, steps

    def _derive_parens(self, depth: int) -> tuple[str, list[str]]:
        """Derive balanced parentheses with leftmost derivation.

        Args:
            depth: Controls nesting depth.

        Returns:
            Tuple of (target_string, derivation_steps).
        """
        steps = []
        current = "S"
        if depth >= 2:
            new = current.replace("S", "(S)", 1)
            steps.append(f"{current} => {new}")
            current = new
        for _ in range(min(depth - 1, 2)):
            if "S" in current:
                new = current.replace("S", "SS", 1)
                steps.append(f"{current} => {new}")
                current = new
                break
        while "S" in current:
            new = current.replace("S", "()", 1)
            steps.append(f"{current} => {new}")
            current = new
        return current, steps

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CFG derivation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        depth = min(2 + difficulty // 2, 5)
        grammar_idx = difficulty % min(len(self._GRAMMARS), 3)
        grammar = self._GRAMMARS[grammar_idx]

        if grammar["family"] == "a^n b^n":
            target, steps = self._derive_anbn(depth)
        elif grammar["family"] == "palindromes":
            target, steps = self._derive_palindrome(self._rng, depth)
        else:
            target, steps = self._derive_parens(depth)

        grammar_spec = _GrammarSpec(
            "S", grammar["rules"]
        )
        problem = f"grammar: {grammar_spec.format_rules()}; derive: {target}"
        return problem, {
            "target": target,
            "derivation": steps,
            "grammar": grammar_spec.format_rules(),
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate derivation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Leftmost derivation steps.
        """
        return solution_data["derivation"]

    def _create_answer(self, solution_data: dict) -> str:
        """Extract the derived string as the final answer.

        Args:
            solution_data: All computed solution information.

        Returns:
            The derived terminal string.
        """
        return solution_data["target"]


# ---------------------------------------------------------------------------
# 4. CFG Ambiguity (tier 6)
# ---------------------------------------------------------------------------

@register
class CFGAmbiguityGenerator(StepGenerator):
    """Find two different leftmost derivations for the same string in an ambiguous grammar.

    Uses well-known ambiguous grammars (e.g., expression grammar E -> E+E | E*E | a)
    and constructs two distinct parse trees for a given string.
    """

    _TEMPLATES: list[dict] = [
        {
            "rules": {"E": ["E+E", "E*E", "a"]},
            "string": "a+a*a",
            "deriv1": [
                "E => E+E", "E+E => a+E", "a+E => a+E*E",
                "a+E*E => a+a*E", "a+a*E => a+a*a",
            ],
            "deriv2": [
                "E => E*E", "E*E => E+E*E", "E+E*E => a+E*E",
                "a+E*E => a+a*E", "a+a*E => a+a*a",
            ],
        },
        {
            "rules": {"S": ["SS", "(S)", "()"]},
            "string": "()()()",
            "deriv1": [
                "S => SS", "SS => SSS", "SSS => ()SS",
                "()SS => ()()S", "()()S => ()()()",
            ],
            "deriv2": [
                "S => SS", "SS => ()S", "()S => ()SS",
                "()SS => ()()S", "()()S => ()()()",
            ],
        },
        {
            "rules": {"S": ["aSb", "aSbb", ""]},
            "string": "aabbb",
            "deriv1": [
                "S => aSb", "aSb => aaSbbb",
                "aaSbbb => aabbb",
            ],
            "deriv2": [
                "S => aSbb", "aSbb => aaSbbb",
                "aaSbbb => aabbb",
            ],
        },
        {
            "rules": {"E": ["E+E", "a", "b"]},
            "string": "a+b+a",
            "deriv1": [
                "E => E+E", "E+E => a+E", "a+E => a+E+E",
                "a+E+E => a+b+E", "a+b+E => a+b+a",
            ],
            "deriv2": [
                "E => E+E", "E+E => E+E+E", "E+E+E => a+E+E",
                "a+E+E => a+b+E", "a+b+E => a+b+a",
            ],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cfg_ambiguity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["cfg_derivation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "find two different leftmost derivations (prove grammar is ambiguous)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CFG ambiguity problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        template = self._TEMPLATES[idx]
        grammar_spec = _GrammarSpec("E" if "E" in template["rules"] else "S",
                                    template["rules"])
        problem = (
            f"grammar: {grammar_spec.format_rules()}; "
            f"string: {template['string']}; "
            f"find two different leftmost derivations"
        )
        return problem, {
            "string": template["string"],
            "deriv1": template["deriv1"],
            "deriv2": template["deriv2"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate steps showing both derivations.

        Args:
            solution_data: All computed solution information.

        Returns:
            Steps listing both derivation sequences.
        """
        steps = ["derivation 1:"]
        steps.extend(f"  {s}" for s in solution_data["deriv1"])
        steps.append("derivation 2:")
        steps.extend(f"  {s}" for s in solution_data["deriv2"])
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        """State that the grammar is ambiguous.

        Args:
            solution_data: All computed solution information.

        Returns:
            Ambiguity verdict.
        """
        return (
            f"AMBIGUOUS: '{solution_data['string']}' has 2 distinct "
            f"leftmost derivations"
        )


# ---------------------------------------------------------------------------
# 5. Pushdown Automaton Simulation (tier 5)
# ---------------------------------------------------------------------------

@register
class PushdownSimulateGenerator(StepGenerator):
    """Simulate a pushdown automaton on an input string.

    Builds small PDAs for languages like a^n b^n, balanced parentheses,
    or ww^R. Shows the stack contents at each step and the final
    accept/reject decision.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pushdown_simulate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["stack_operations", "dfa_accept"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "simulate pushdown automaton (show stack at each step)"

    def _build_anbn_pda(self, n: int,
                        accept: bool) -> tuple[str, list[dict], bool]:
        """Build a PDA trace for a^n b^n recognition.

        Args:
            n: Number of a's (and b's if accepting).
            accept: Whether the string should be accepted.

        Returns:
            Tuple of (input_string, trace_entries, accepted).
        """
        if accept:
            input_str = "a" * n + "b" * n
        else:
            extra = self._rng.randint(1, 2)
            input_str = "a" * n + "b" * (n + extra)

        trace: list[dict] = []
        stack = ["Z"]
        state = "q0"
        accepted = True

        for sym in input_str:
            entry = {"state": state, "input": sym, "stack_before": list(stack)}
            if state == "q0" and sym == "a":
                stack.append("A")
                entry["action"] = "push A"
                entry["stack_after"] = list(stack)
            elif state == "q0" and sym == "b":
                state = "q1"
                if stack and stack[-1] == "A":
                    stack.pop()
                    entry["action"] = "pop A, goto q1"
                else:
                    accepted = False
                    entry["action"] = "REJECT (no A to pop)"
                    entry["stack_after"] = list(stack)
                    trace.append(entry)
                    break
                entry["stack_after"] = list(stack)
            elif state == "q1" and sym == "b":
                if stack and stack[-1] == "A":
                    stack.pop()
                    entry["action"] = "pop A"
                else:
                    accepted = False
                    entry["action"] = "REJECT (no A to pop)"
                    entry["stack_after"] = list(stack)
                    trace.append(entry)
                    break
                entry["stack_after"] = list(stack)
            else:
                accepted = False
                entry["action"] = "REJECT (unexpected)"
                entry["stack_after"] = list(stack)
                trace.append(entry)
                break
            trace.append(entry)

        if accepted and stack != ["Z"]:
            accepted = False

        return input_str, trace, accepted

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PDA simulation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = min(2 + difficulty // 2, 5)
        do_accept = self._rng.choice([True, False])
        input_str, trace, accepted = self._build_anbn_pda(n, do_accept)

        rules_str = (
            "(q0,a,Z)->push A; (q0,a,A)->push A; "
            "(q0,b,A)->pop,goto q1; (q1,b,A)->pop; "
            "(q1,eps,Z)->ACCEPT"
        )
        problem = f"PDA for a^n b^n: {rules_str}; input='{input_str}'"
        return problem, {
            "input": input_str,
            "trace": trace,
            "accepted": accepted,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate steps showing stack at each transition.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings showing state, input, and stack.
        """
        steps = []
        for entry in solution_data["trace"]:
            stack_str = "".join(entry.get("stack_after", []))
            steps.append(
                f"({entry['state']},'{entry['input']}') {entry['action']} "
                f"stack=[{stack_str}]"
            )
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        """Return accept/reject verdict.

        Args:
            solution_data: All computed solution information.

        Returns:
            ACCEPT or REJECT.
        """
        return "ACCEPT" if solution_data["accepted"] else "REJECT"


# ---------------------------------------------------------------------------
# 6. Pumping Lemma (tier 6)
# ---------------------------------------------------------------------------

@register
class PumpingLemmaGenerator(StepGenerator):
    """Prove a language is not regular using the pumping lemma.

    Chooses a non-regular language, picks a pumping string s, shows that
    for all decompositions s=xyz with |xy|<=p and |y|>0, there exists
    an i such that xy^iz is not in L.
    """

    _LANGUAGES: list[dict] = [
        {
            "desc": "L = {a^n b^n | n >= 0}",
            "s_template": "a^p b^p",
            "proof": [
                "let p be pumping length, s = a^p b^p, |s| = 2p >= p",
                "for any split s=xyz with |xy|<=p, |y|>0: y = a^k (k>=1)",
                "pump down: i=0, xz = a^(p-k) b^p",
                "p-k != p so a^(p-k) b^p not in L",
            ],
            "conclusion": "L is not regular",
        },
        {
            "desc": "L = {ww | w in {a,b}*}",
            "s_template": "a^p b a^p b",
            "proof": [
                "let p be pumping length, s = a^p b a^p b, |s| >= p",
                "for any split s=xyz with |xy|<=p, |y|>0: y = a^k (k>=1)",
                "pump up: i=2, xy^2z = a^(p+k) b a^p b",
                "first half != second half, so not in L",
            ],
            "conclusion": "L is not regular",
        },
        {
            "desc": "L = {a^(n^2) | n >= 0}",
            "s_template": "a^(p^2)",
            "proof": [
                "let p be pumping length, s = a^(p^2), |s| >= p",
                "for any split s=xyz with |xy|<=p, |y|>0: |y| = k, 1<=k<=p",
                "pump up: i=2, |xy^2z| = p^2 + k",
                "p^2 < p^2+k <= p^2+p < (p+1)^2, so not a perfect square",
            ],
            "conclusion": "L is not regular",
        },
        {
            "desc": "L = {a^n b^m | n > m >= 0}",
            "s_template": "a^(p+1) b^p",
            "proof": [
                "let p be pumping length, s = a^(p+1) b^p, |s| >= p",
                "for any split s=xyz with |xy|<=p, |y|>0: y = a^k (k>=1)",
                "pump down: i=0, xz = a^(p+1-k) b^p",
                "when k>=2: p+1-k <= p-1 < p, violates n>m condition",
            ],
            "conclusion": "L is not regular",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pumping_lemma"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["proof_by_contradiction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "prove language is not regular using pumping lemma"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a pumping lemma proof problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._LANGUAGES)
        lang = self._LANGUAGES[idx]
        problem = f"{lang['desc']}; prove not regular using pumping lemma"
        return problem, {
            "desc": lang["desc"],
            "s_template": lang["s_template"],
            "proof": lang["proof"],
            "conclusion": lang["conclusion"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate pumping lemma proof steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Proof steps.
        """
        return solution_data["proof"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the conclusion.

        Args:
            solution_data: All computed solution information.

        Returns:
            Statement that the language is not regular.
        """
        return solution_data["conclusion"]


# ---------------------------------------------------------------------------
# 7. Chomsky Normal Form (tier 6)
# ---------------------------------------------------------------------------

@register
class ChomskyNormalFormGenerator(StepGenerator):
    """Convert a context-free grammar to Chomsky Normal Form.

    Applies the standard CNF conversion steps: eliminate epsilon
    productions, eliminate unit productions, and break long rules into
    binary productions. Uses small grammars to keep output under 512 chars.
    """

    _TEMPLATES: list[dict] = [
        {
            "rules": {"S": ["aSb", "ab"]},
            "cnf_steps": [
                "introduce terminals: A->a, B->b",
                "S -> aSb becomes S -> A S1, S1 -> S B",
                "S -> ab becomes S -> A B",
            ],
            "cnf_rules": {"S": ["A S1", "A B"], "S1": ["S B"],
                          "A": ["a"], "B": ["b"]},
        },
        {
            "rules": {"S": ["AB", "a"], "A": ["aA", "a"], "B": ["bB", "b"]},
            "cnf_steps": [
                "introduce terminals: Ta->a, Tb->b",
                "A -> aA becomes A -> Ta A (already binary)",
                "B -> bB becomes B -> Tb B (already binary)",
                "no epsilon or unit rules to remove",
            ],
            "cnf_rules": {"S": ["A B", "a"], "A": ["Ta A", "a"],
                          "B": ["Tb B", "b"], "Ta": ["a"], "Tb": ["b"]},
        },
        {
            "rules": {"S": ["aXb", "ab"], "X": ["aXb", "ab"]},
            "cnf_steps": [
                "introduce terminals: A->a, B->b",
                "S -> aXb becomes S -> A S1, S1 -> X B",
                "S -> ab becomes S -> A B",
                "X -> aXb becomes X -> A X1, X1 -> X B",
                "X -> ab becomes X -> A B",
            ],
            "cnf_rules": {"S": ["A S1", "A B"], "S1": ["X B"],
                          "X": ["A X1", "A B"], "X1": ["X B"],
                          "A": ["a"], "B": ["b"]},
        },
        {
            "rules": {"S": ["ABa", "a"], "A": ["aA", "a"], "B": ["b"]},
            "cnf_steps": [
                "introduce terminal: Ta->a",
                "S -> ABa: break into S -> A S1, S1 -> B Ta",
                "A -> aA becomes A -> Ta A",
                "no epsilon or unit rules",
            ],
            "cnf_rules": {"S": ["A S1", "a"], "S1": ["B Ta"],
                          "A": ["Ta A", "a"], "B": ["b"], "Ta": ["a"]},
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chomsky_normal"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["cfg_derivation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "convert grammar to Chomsky Normal Form"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CNF conversion problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        template = self._TEMPLATES[idx]
        grammar = _GrammarSpec("S", template["rules"])
        problem = f"convert to CNF: {grammar.format_rules()}"
        cnf_grammar = _GrammarSpec("S", template["cnf_rules"])
        return problem, {
            "original": grammar.format_rules(),
            "cnf_steps": template["cnf_steps"],
            "cnf_rules": cnf_grammar.format_rules(),
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate CNF conversion steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings describing each transformation.
        """
        return solution_data["cnf_steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the CNF grammar.

        Args:
            solution_data: All computed solution information.

        Returns:
            The grammar in Chomsky Normal Form.
        """
        return f"CNF: {solution_data['cnf_rules']}"


# ---------------------------------------------------------------------------
# 8. Language Classification (tier 6)
# ---------------------------------------------------------------------------

@register
class LanguageClassifyGenerator(StepGenerator):
    """Classify a language in the Chomsky hierarchy.

    Given a language description, determine whether it is regular,
    context-free, context-sensitive, or recursively enumerable. Provides
    justification based on structural properties of the language.
    """

    _LANGUAGES: list[dict] = [
        {
            "desc": "L = {a^n | n >= 0}",
            "classification": "regular",
            "reason": "matched by regex a*; DFA with 1 state",
            "tier_label": "Type 3 (regular)",
        },
        {
            "desc": "L = {a^n b^n | n >= 1}",
            "classification": "context-free",
            "reason": "generated by CFG S->aSb|ab; not regular (pumping lemma)",
            "tier_label": "Type 2 (context-free)",
        },
        {
            "desc": "L = {a^n b^n c^n | n >= 1}",
            "classification": "context-sensitive",
            "reason": "not CF (pumping lemma for CFLs); CSG exists using markers",
            "tier_label": "Type 1 (context-sensitive)",
        },
        {
            "desc": "L = {w | w encodes a halting TM}",
            "classification": "recursively enumerable",
            "reason": "TM can simulate and accept if halts; undecidable complement",
            "tier_label": "Type 0 (recursively enumerable)",
        },
        {
            "desc": "L = (a|b)* (strings over {a,b})",
            "classification": "regular",
            "reason": "matched by regex (a|b)*; trivial 1-state DFA accepts all",
            "tier_label": "Type 3 (regular)",
        },
        {
            "desc": "L = {ww^R | w in {a,b}*}",
            "classification": "context-free",
            "reason": "CFG S->aSa|bSb|eps; needs stack but not LBA",
            "tier_label": "Type 2 (context-free)",
        },
        {
            "desc": "L = {ww | w in {a,b}*}",
            "classification": "context-sensitive",
            "reason": "not CF (pumping lemma for CFLs); LBA can verify by marking",
            "tier_label": "Type 1 (context-sensitive)",
        },
        {
            "desc": "L = {a^p | p is prime}",
            "classification": "context-sensitive",
            "reason": "not CF (pumping); LBA can check primality of length",
            "tier_label": "Type 1 (context-sensitive)",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "language_classify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["chomsky_normal"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "classify language in Chomsky hierarchy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a language classification problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._LANGUAGES)
        lang = self._LANGUAGES[idx]
        problem = f"{lang['desc']}; classify in Chomsky hierarchy"
        return problem, {
            "desc": lang["desc"],
            "classification": lang["classification"],
            "reason": lang["reason"],
            "tier_label": lang["tier_label"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate classification reasoning steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings explaining the classification.
        """
        return [
            f"language: {solution_data['desc']}",
            f"analysis: {solution_data['reason']}",
            f"classification: {solution_data['tier_label']}",
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the Chomsky hierarchy classification.

        Args:
            solution_data: All computed solution information.

        Returns:
            The classification label.
        """
        return solution_data["tier_label"]
