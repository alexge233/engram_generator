"""Extended automata and formal language generators.

6 generators across tiers 4-6.
"""

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class MealyMachineGenerator(StepGenerator):
    """Simulate a Mealy machine on an input string.

    Output depends on both the current state and the input symbol.
    Given transition and output tables, computes the output string.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mealy_machine"

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
        return "simulate Mealy machine"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Mealy machine and simulate on input.

        Args:
            difficulty: Difficulty level controlling state count and input length.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        n_states = min(2 + difficulty // 2, 4)
        symbols = "ab"
        out_symbols = "01"
        transitions = {}
        outputs = {}
        for s in range(n_states):
            for sym in symbols:
                transitions[(s, sym)] = self._rng.randint(0, n_states - 1)
                outputs[(s, sym)] = self._rng.choice(out_symbols)
        length = min(3 + difficulty, 8)
        input_str = "".join(self._rng.choice(symbols) for _ in range(length))
        state = 0
        trace = []
        output_str = ""
        for sym in input_str:
            out = outputs[(state, sym)]
            next_state = transitions[(state, sym)]
            trace.append(f"q{state}+{sym}->q{next_state}/{out}")
            output_str += out
            state = next_state
        trans_str = "; ".join(
            f"(q{s},{sym})->q{transitions[(s,sym)]}/{outputs[(s,sym)]}"
            for s in range(n_states) for sym in symbols
        )
        problem = (
            f"Mealy: states=q0..q{n_states-1}, {trans_str}. "
            f"input='{input_str}'. output?"
        )
        return problem, {
            "input": input_str, "trace": trace,
            "output": output_str, "final_state": state,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show step-by-step Mealy machine simulation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Return the output string.

        Args:
            sd: Solution data dict.

        Returns:
            Output string produced by the Mealy machine.
        """
        return sd["output"]


@register
class MooreMachineGenerator(StepGenerator):
    """Simulate a Moore machine on an input string.

    Output depends only on the current state. Given transition table
    and state output mapping, computes the output string.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "moore_machine"

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
        return "simulate Moore machine"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Moore machine and simulate on input.

        Args:
            difficulty: Difficulty level controlling state count and input length.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        n_states = min(2 + difficulty // 2, 4)
        symbols = "ab"
        out_symbols = "01"
        transitions = {}
        state_output = {}
        for s in range(n_states):
            state_output[s] = self._rng.choice(out_symbols)
            for sym in symbols:
                transitions[(s, sym)] = self._rng.randint(0, n_states - 1)
        length = min(3 + difficulty, 8)
        input_str = "".join(self._rng.choice(symbols) for _ in range(length))
        state = 0
        trace = []
        output_str = state_output[state]
        trace.append(f"q{state}->out={state_output[state]}")
        for sym in input_str:
            next_state = transitions[(state, sym)]
            out = state_output[next_state]
            trace.append(f"q{state}+{sym}->q{next_state}->out={out}")
            output_str += out
            state = next_state
        trans_str = "; ".join(
            f"(q{s},{sym})->q{transitions[(s,sym)]}"
            for s in range(n_states) for sym in symbols
        )
        out_str = ", ".join(f"q{s}->{state_output[s]}" for s in range(n_states))
        problem = (
            f"Moore: {trans_str}. outputs: {out_str}. "
            f"input='{input_str}'. output?"
        )
        return problem, {
            "input": input_str, "trace": trace,
            "output": output_str, "final_state": state,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show step-by-step Moore machine simulation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Return the output string.

        Args:
            sd: Solution data dict.

        Returns:
            Output string produced by the Moore machine.
        """
        return sd["output"]


@register
class TransducerGenerator(StepGenerator):
    """Simulate a finite state transducer on an input string.

    Reads input symbols and produces output symbols per transition.
    Combines aspects of Mealy machines with potentially multi-character output.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "transducer"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["mealy_machine"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "simulate finite state transducer"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a transducer and apply to input.

        Args:
            difficulty: Difficulty level controlling state count and input length.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        n_states = min(2 + difficulty // 2, 4)
        in_symbols = "01"
        out_options = ["x", "y", "xy", "yx", "xx", "yy"]
        transitions = {}
        trans_outputs = {}
        for s in range(n_states):
            for sym in in_symbols:
                transitions[(s, sym)] = self._rng.randint(0, n_states - 1)
                trans_outputs[(s, sym)] = self._rng.choice(out_options[:2 + difficulty])
        length = min(3 + difficulty, 7)
        input_str = "".join(self._rng.choice(in_symbols) for _ in range(length))
        state = 0
        trace = []
        output_str = ""
        for sym in input_str:
            out = trans_outputs[(state, sym)]
            next_state = transitions[(state, sym)]
            trace.append(f"q{state}+{sym}->q{next_state}/'{out}'")
            output_str += out
            state = next_state
        trans_str = "; ".join(
            f"(q{s},{sym})->q{transitions[(s,sym)]}/'{trans_outputs[(s,sym)]}'"
            for s in range(n_states) for sym in in_symbols
        )
        problem = (
            f"FST: {trans_str}. input='{input_str}'. output?"
        )
        return problem, {
            "input": input_str, "trace": trace,
            "output": output_str, "final_state": state,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show step-by-step transducer simulation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return sd["trace"]

    def _create_answer(self, sd: dict) -> str:
        """Return the transducer output string.

        Args:
            sd: Solution data dict.

        Returns:
            Output string.
        """
        return sd["output"]


@register
class DFAMinimizationGenerator(StepGenerator):
    """Minimize a DFA by identifying and merging equivalent states.

    Uses the table-filling (Myhill-Nerode) algorithm to find
    distinguishable state pairs, then merges equivalent states.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dfa_minimization"

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
        return "minimize DFA by table-filling"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DFA with redundant states and minimize it.

        Args:
            difficulty: Difficulty level controlling state count.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        n_states = min(3 + difficulty // 2, 5)
        accept = set()
        accept.add(self._rng.randint(1, n_states - 1))
        if self._rng.random() < 0.4:
            accept.add(self._rng.randint(0, n_states - 1))
        transitions = {}
        for s in range(n_states):
            for sym in "01":
                transitions[(s, sym)] = self._rng.randint(0, n_states - 1)

        # Table-filling algorithm
        distinguishable = set()
        # Initial: accept vs non-accept
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

        # Equivalent pairs
        equiv_pairs = []
        for i in range(n_states):
            for j in range(i + 1, n_states):
                if (i, j) not in distinguishable:
                    equiv_pairs.append((i, j))

        # Count equivalence classes using union-find
        parent = list(range(n_states))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i, j in equiv_pairs:
            ri, rj = find(i), find(j)
            if ri != rj:
                parent[rj] = ri

        classes = {}
        for s in range(n_states):
            root = find(s)
            if root not in classes:
                classes[root] = []
            classes[root].append(s)

        min_states = len(classes)
        trans_str = "; ".join(
            f"(q{s},{sym})->q{transitions[(s,sym)]}"
            for s in range(n_states) for sym in "01"
        )
        problem = (
            f"DFA: q0..q{n_states-1}, accept={sorted(accept)}, "
            f"{trans_str}. minimize?"
        )
        return problem, {
            "n_states": n_states, "accept": sorted(accept),
            "transitions": {f"(q{s},{sym})": f"q{transitions[(s,sym)]}"
                            for s in range(n_states) for sym in "01"},
            "equiv_pairs": equiv_pairs,
            "classes": {f"q{k}": [f"q{s}" for s in v] for k, v in classes.items()},
            "min_states": min_states,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show table-filling minimization steps.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = [
            f"original: {sd['n_states']} states, accept={sd['accept']}",
            f"equivalent pairs: {sd['equiv_pairs']}",
        ]
        for rep, members in sd["classes"].items():
            steps.append(f"class {rep}: {members}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the minimized DFA state count.

        Args:
            sd: Solution data dict.

        Returns:
            Minimized state count and equivalence classes.
        """
        return f"minimized: {sd['min_states']} states"


@register
class PumpingLemmaCFLGenerator(StepGenerator):
    """Apply the CFL pumping lemma to show a language is not context-free.

    Uses a template-based approach: picks a known non-CFL language,
    generates a pumping argument with specific string decomposition.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pumping_lemma_cfl"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["nfa_simulate"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply CFL pumping lemma"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CFL pumping lemma proof template.

        Args:
            difficulty: Difficulty level controlling pumping length.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        templates = [
            {
                "lang": "a^n b^n c^n",
                "desc": "{a^n b^n c^n | n >= 0}",
                "gen_s": lambda p: "a" * p + "b" * p + "c" * p,
                "reason": "pumping changes count of at most 2 symbols, breaking a^n=b^n=c^n",
            },
            {
                "lang": "a^n b^n c^n d^n",
                "desc": "{a^n b^n c^n d^n | n >= 0}",
                "gen_s": lambda p: "a" * p + "b" * p + "c" * p + "d" * p,
                "reason": "vxy spans at most 2 symbol types, pumping breaks equality",
            },
            {
                "lang": "ww",
                "desc": "{ww | w in {a,b}*}",
                "gen_s": lambda p: "a" * p + "b" * p + "a" * p + "b" * p,
                "reason": "pumping v and y disrupts the ww structure",
            },
        ]
        template = self._rng.choice(templates)
        p = min(2 + difficulty, 6)
        s = template["gen_s"](p)
        # Decompose s = uvxyz with |vxy| <= p, |vy| >= 1
        # Pick a decomposition to demonstrate
        v_start = self._rng.randint(0, min(p - 1, len(s) - 2))
        v_len = self._rng.randint(1, min(2, len(s) - v_start - 1))
        y_start = v_start + v_len + self._rng.randint(0, min(1, p - v_len - 1))
        y_len = max(1, min(2, len(s) - y_start))
        if y_start + y_len > len(s):
            y_len = len(s) - y_start
        v = s[v_start:v_start + v_len]
        y = s[y_start:y_start + y_len]
        # Pump i=2
        pumped = s[:v_start] + v * 2 + s[v_start + v_len:y_start] + y * 2 + s[y_start + y_len:]

        problem = (
            f"L = {template['desc']}. p={p}, s={s}. "
            f"show not CFL by pumping."
        )
        return problem, {
            "lang": template["lang"], "p": p, "s": s,
            "v": v, "y": y, "pumped": pumped,
            "reason": template["reason"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show pumping lemma argument.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"choose s = {sd['s']} in L, |s| >= p={sd['p']}",
            f"any decomposition: v='{sd['v']}', y='{sd['y']}'",
            f"pump i=2: {sd['pumped']} not in L",
            sd["reason"],
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the pumping lemma conclusion.

        Args:
            sd: Solution data dict.

        Returns:
            Statement that L is not context-free.
        """
        return f"{sd['lang']} is not CFL"


@register
class TwoStackPDAGenerator(StepGenerator):
    """Simulate a 2-stack PDA on simple input.

    A 2-stack PDA is equivalent to a Turing machine. Simulates
    transitions that read input and manipulate two stacks.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "two_stack_pda"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["turing_machine_step"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "simulate 2-stack PDA"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2-stack PDA and simulate on input.

        Simple machine: phase 1 pushes input onto stack1,
        phase 2 transfers from stack1 to stack2 checking/transforming.

        Args:
            difficulty: Difficulty level controlling input length.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        length = min(3 + difficulty, 7)
        input_str = "".join(self._rng.choice("ab") for _ in range(length))
        # Simple 2-stack PDA: push to stack1, then pop all to stack2
        # State q0: read input, push to stack1
        # State q1: pop stack1, push to stack2 (reverses)
        # State q2: accept if both stacks empty and input consumed
        stack1 = []
        stack2 = []
        state = "q0"
        trace = []

        # Phase 1: push input onto stack1
        for sym in input_str:
            stack1.append(sym)
            trace.append(f"{state}: read '{sym}', push S1 -> S1={list(stack1)}")

        state = "q1"
        trace.append(f"transition to {state}")

        # Phase 2: transfer stack1 to stack2
        steps_phase2 = min(len(stack1), 3 + difficulty)
        for _ in range(steps_phase2):
            if not stack1:
                break
            sym = stack1.pop()
            stack2.append(sym)
            trace.append(f"{state}: pop S1='{sym}', push S2 -> S2={list(stack2)}")

        if not stack1:
            state = "q2"
            accepted = True
        else:
            accepted = False

        problem = (
            f"2-stack PDA: input='{input_str}'. "
            f"q0:push S1, q1:S1->S2, q2:accept. simulate."
        )
        return problem, {
            "input": input_str, "trace": trace,
            "stack1": list(stack1), "stack2": list(stack2),
            "final_state": state, "accepted": accepted,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show 2-stack PDA simulation steps (truncated for length).

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        trace = sd["trace"]
        return trace[:5] if len(trace) > 5 else trace

    def _create_answer(self, sd: dict) -> str:
        """Return the final configuration.

        Args:
            sd: Solution data dict.

        Returns:
            Final state and stack contents.
        """
        return (
            f"state={sd['final_state']}, "
            f"S1={sd['stack1']}, S2={sd['stack2']}"
        )
