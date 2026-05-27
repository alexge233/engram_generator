"""Automata and formal language generators.

3 generators across tiers 3-4.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class DFAAcceptGenerator(StepGenerator):
    """Simulate a DFA on an input string."""

    @property
    def task_name(self) -> str:
        return "dfa_accept"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        return "simulate DFA"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_states = min(3 + difficulty // 2, 6)
        accept_states = {self._rng.randint(1, n_states - 1)}
        transitions = {}
        for s in range(n_states):
            for sym in "01":
                transitions[(s, sym)] = self._rng.randint(0, n_states - 1)
        length = min(3 + difficulty, 10)
        input_str = "".join(self._rng.choice("01") for _ in range(length))
        state = 0
        trace = [state]
        for sym in input_str:
            state = transitions[(state, sym)]
            trace.append(state)
        accepted = state in accept_states
        trans_str = "; ".join(f"({s},{sym})->{transitions[(s,sym)]}" for s in range(n_states) for sym in "01")
        return (
            f"states=0..{n_states-1}, accept={accept_states}, input='{input_str}', transitions: {trans_str}",
            {"input": input_str, "trace": trace, "accepted": accepted, "accept_states": accept_states},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for i, sym in enumerate(sd["input"]):
            steps.append(f"state {sd['trace'][i]} + '{sym}' -> state {sd['trace'][i+1]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return "ACCEPT" if sd["accepted"] else "REJECT"


@register
class NFASimulateGenerator(StepGenerator):
    """Simulate an NFA (track set of states)."""

    @property
    def task_name(self) -> str:
        return "nfa_simulate"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["dfa_accept", "set_union"]

    def task_description(self, difficulty: int) -> str:
        return "simulate NFA"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_states = min(3 + difficulty // 2, 5)
        accept_states = {self._rng.randint(1, n_states - 1)}
        transitions = {}
        for s in range(n_states):
            for sym in "01":
                n_targets = self._rng.randint(0, 2)
                transitions[(s, sym)] = set(self._rng.sample(range(n_states), min(n_targets, n_states)))
        length = min(2 + difficulty, 6)
        input_str = "".join(self._rng.choice("01") for _ in range(length))
        current = {0}
        trace = [frozenset(current)]
        for sym in input_str:
            nxt = set()
            for s in current:
                nxt |= transitions.get((s, sym), set())
            current = nxt
            trace.append(frozenset(current))
        accepted = bool(current & accept_states)
        return (
            f"NFA: states=0..{n_states-1}, accept={accept_states}, input='{input_str}'",
            {"input": input_str, "trace": [set(t) for t in trace], "accepted": accepted},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for i, sym in enumerate(sd["input"]):
            steps.append(f"{sd['trace'][i]} + '{sym}' -> {sd['trace'][i+1]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return "ACCEPT" if sd["accepted"] else "REJECT"


@register
class TuringMachineStepGenerator(StepGenerator):
    """Execute steps of a simple Turing machine."""

    @property
    def task_name(self) -> str:
        return "turing_machine_step"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["dfa_accept"]

    def task_description(self, difficulty: int) -> str:
        return "execute Turing machine steps"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        tape = list("".join(self._rng.choice("01") for _ in range(min(5 + difficulty, 10))))
        rules = {
            ("q0", "0"): ("q0", "1", "R"),
            ("q0", "1"): ("q1", "0", "R"),
            ("q1", "0"): ("q1", "0", "R"),
            ("q1", "1"): ("q0", "1", "L"),
            ("q0", "_"): ("halt", "_", "S"),
            ("q1", "_"): ("halt", "_", "S"),
        }
        state = "q0"
        head = 0
        n_steps = min(3 + difficulty, 8)
        steps_log = []
        for _ in range(n_steps):
            sym = tape[head] if head < len(tape) else "_"
            if (state, sym) not in rules:
                break
            new_state, write, move = rules[(state, sym)]
            if head < len(tape):
                tape[head] = write
            steps_log.append(f"({state},{sym})->({new_state},{write},{move})")
            state = new_state
            if move == "R":
                head += 1
            elif move == "L":
                head = max(0, head - 1)
            if state == "halt":
                break
        return (
            f"tape={''.join(tape[:10])}, run {n_steps} steps",
            {"tape": "".join(tape[:10]), "steps_log": steps_log, "final_state": state},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        return f"tape={sd['tape']}, state={sd['final_state']}"
