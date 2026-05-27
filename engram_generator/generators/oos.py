"""Out-of-set generators for held-out evaluation.

These tasks are NEVER used in training or validation. They test
whether the model can transfer reasoning to structurally novel
domains it has never seen.

Each generator shares reasoning structure with trained tasks
but uses completely different surface form.
"""
import math
import random

from engram_generator.base import Sample, StepGenerator, STEP_TOKEN
from engram_generator.curriculum.registry import register_oos


@register_oos
class SymbolicLogicGenerator(StepGenerator):
    """Propositional logic proof chains.

    Shares structure with: equation solving, algebraic simplification.
    Requires: chaining rules, maintaining truth state.
    """

    @property
    def task_name(self) -> str:
        return "oos_symbolic_logic"

    @property
    def tier(self) -> int:
        return 99

    def task_description(self, difficulty: int) -> str:
        return "evaluate logic proof"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a propositional logic evaluation problem.

        Args:
            difficulty: Controls number of premises and rule applications.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        num_vars = min(2 + difficulty // 2, 6)
        variables = [chr(ord('P') + i) for i in range(num_vars)]
        assignments = {v: self._rng.choice([True, False]) for v in variables}

        rules = self._build_rules(variables, difficulty)
        derived = self._apply_rules(assignments, rules)

        query_var = self._rng.choice(list(derived.keys()))
        problem = self._format_premises(assignments, rules, query_var)

        return problem, {
            "assignments": assignments,
            "rules": rules,
            "derived": derived,
            "query": query_var,
            "answer": derived[query_var],
        }

    def _build_rules(self, variables: list[str],
                     difficulty: int) -> list[dict]:
        """Build inference rules from variables.

        Args:
            variables: Available variable names.
            difficulty: Controls rule complexity.

        Returns:
            List of rule dicts with 'type', 'premises', 'conclusion'.
        """
        rules = []
        num_rules = min(1 + difficulty, 5)

        for _ in range(num_rules):
            rule_type = self._rng.choice(["modus_ponens", "and_intro", "or_elim"])
            a = self._rng.choice(variables)
            b = self._rng.choice(variables)
            if a == b:
                b = variables[(variables.index(a) + 1) % len(variables)]

            if rule_type == "modus_ponens":
                conclusion = f"Z{len(rules)}"
                rules.append({
                    "type": "modus_ponens",
                    "if": a, "then": conclusion,
                    "text": f"if {a} then {conclusion}",
                })
            elif rule_type == "and_intro":
                conclusion = f"{a} AND {b}"
                rules.append({
                    "type": "and",
                    "left": a, "right": b,
                    "conclusion": conclusion,
                    "text": f"{a} AND {b} = {conclusion}",
                })
            else:
                rules.append({
                    "type": "or",
                    "left": a, "right": b,
                    "text": f"{a} OR {b}",
                })

        return rules

    def _apply_rules(self, assignments: dict,
                     rules: list[dict]) -> dict:
        """Apply rules to derive new truth values.

        Args:
            assignments: Initial variable assignments.
            rules: Inference rules.

        Returns:
            Extended assignment dict with derived values.
        """
        derived = dict(assignments)
        for rule in rules:
            if rule["type"] == "modus_ponens":
                if derived.get(rule["if"], False):
                    derived[rule["then"]] = True
                else:
                    derived[rule["then"]] = False
            elif rule["type"] == "and":
                val = derived.get(rule["left"], False) and derived.get(rule["right"], False)
                derived[rule["conclusion"]] = val
            elif rule["type"] == "or":
                key = f"{rule['left']} OR {rule['right']}"
                val = derived.get(rule["left"], False) or derived.get(rule["right"], False)
                derived[key] = val
        return derived

    def _format_premises(self, assignments: dict, rules: list[dict],
                         query: str) -> str:
        """Format the problem as a string.

        Args:
            assignments: Variable truth values.
            rules: Inference rules.
            query: Variable to query.

        Returns:
            Formatted problem string.
        """
        parts = []
        for var, val in assignments.items():
            parts.append(f"{var}={'T' if val else 'F'}")
        for rule in rules:
            parts.append(rule["text"])
        parts.append(f"? {query}")
        return "; ".join(parts)

    def _create_steps(self, solution_data: dict) -> list[str]:
        steps = []
        for rule in solution_data["rules"]:
            steps.append(f"apply {rule['type']}: {rule['text']}")
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        return "T" if solution_data["answer"] else "F"


@register_oos
class UnitConversionGenerator(StepGenerator):
    """Multi-step unit conversion chains.

    Shares structure with: base conversion, multiplication chains.
    Requires: iterative scaling with carry.
    """

    _CHAINS = {
        "length_metric": [("km", "m", 1000), ("m", "cm", 100), ("cm", "mm", 10)],
        "mass_metric": [("kg", "g", 1000), ("g", "mg", 1000)],
        "time": [("hr", "min", 60), ("min", "sec", 60)],
        "length_imperial": [("mi", "yd", 1760), ("yd", "ft", 3), ("ft", "in", 12)],
        "digital": [("TB", "GB", 1024), ("GB", "MB", 1024), ("MB", "KB", 1024)],
    }

    @property
    def task_name(self) -> str:
        return "oos_unit_conversion"

    @property
    def tier(self) -> int:
        return 99

    def task_description(self, difficulty: int) -> str:
        return "convert units"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a unit conversion chain problem.

        Args:
            difficulty: Controls chain length and value magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        chain_name = self._rng.choice(list(self._CHAINS.keys()))
        chain = self._CHAINS[chain_name]
        num_steps = min(1 + difficulty // 2, len(chain))
        chain = chain[:num_steps]

        value = self._rng.randint(1, 5 + difficulty * 2)
        from_unit = chain[0][0]
        to_unit = chain[-1][1]

        steps = []
        current = value
        for from_u, to_u, factor in chain:
            result = current * factor
            steps.append(f"{current} {from_u} = {result} {to_u}")
            current = result

        problem = f"{value} {from_unit} to {to_unit}"
        return problem, {"steps": steps, "answer": current, "to_unit": to_unit}

    def _create_steps(self, solution_data: dict) -> list[str]:
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        return f"{solution_data['answer']} {solution_data['to_unit']}"


@register_oos
class StateMachineGenerator(StepGenerator):
    """Finite state machine simulation.

    Shares structure with: Markov chains, graph traversal.
    Requires: maintaining current state, looking up transitions.
    """

    @property
    def task_name(self) -> str:
        return "oos_state_machine"

    @property
    def tier(self) -> int:
        return 99

    def task_description(self, difficulty: int) -> str:
        return "trace state machine"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a state machine trace problem.

        Args:
            difficulty: Controls number of states and input length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        num_states = min(2 + difficulty // 2, 5)
        states = [f"S{i}" for i in range(num_states)]
        alphabet = ["0", "1"]
        input_len = min(2 + difficulty, 8)

        transitions = {}
        for state in states:
            for symbol in alphabet:
                next_state = self._rng.choice(states)
                transitions[(state, symbol)] = next_state

        input_str = "".join(self._rng.choice(alphabet) for _ in range(input_len))
        trace = self._simulate(states[0], input_str, transitions)

        trans_str = self._format_transitions(transitions)
        problem = f"states={','.join(states)}; {trans_str}; start=S0; input={input_str}"

        return problem, {
            "trace": trace,
            "input": input_str,
            "transitions": transitions,
        }

    def _simulate(self, start: str, input_str: str,
                  transitions: dict) -> list[str]:
        """Simulate the state machine.

        Args:
            start: Initial state.
            input_str: Input symbols.
            transitions: Transition function.

        Returns:
            List of states visited.
        """
        trace = [start]
        current = start
        for symbol in input_str:
            current = transitions[(current, symbol)]
            trace.append(current)
        return trace

    def _format_transitions(self, transitions: dict) -> str:
        """Format transition table as string.

        Args:
            transitions: Dict of (state, symbol) -> next_state.

        Returns:
            Compact transition string.
        """
        parts = []
        for (state, symbol), next_state in sorted(transitions.items()):
            parts.append(f"{state},{symbol}->{next_state}")
        return "; ".join(parts)

    def _create_steps(self, solution_data: dict) -> list[str]:
        trace = solution_data["trace"]
        input_str = solution_data["input"]
        steps = []
        for i, symbol in enumerate(input_str):
            steps.append(f"{trace[i]} + '{symbol}' -> {trace[i + 1]}")
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        return solution_data["trace"][-1]


@register_oos
class ProgramTraceGenerator(StepGenerator):
    """Simple pseudocode program tracing.

    Shares structure with: RPN evaluation, variable tracking.
    Requires: sequential state updates, conditionals.
    """

    @property
    def task_name(self) -> str:
        return "oos_program_trace"

    @property
    def tier(self) -> int:
        return 99

    def task_description(self, difficulty: int) -> str:
        return "trace program output"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a program tracing problem.

        Args:
            difficulty: Controls number of operations and variables.

        Returns:
            Tuple of (program_text, solution_data).
        """
        program_type = self._rng.choice(["accumulator", "swap", "conditional"])

        if program_type == "accumulator":
            return self._accumulator_program(difficulty)
        elif program_type == "swap":
            return self._swap_program(difficulty)
        else:
            return self._conditional_program(difficulty)

    def _accumulator_program(self, difficulty: int) -> tuple[str, dict]:
        """Generate an accumulator loop program.

        Args:
            difficulty: Controls loop iterations.

        Returns:
            Tuple of (program_text, solution_data).
        """
        init = self._rng.randint(0, 5)
        num_ops = min(2 + difficulty, 6)
        ops = []
        x = init
        steps = [f"x = {init}"]

        for _ in range(num_ops):
            op = self._rng.choice(["add", "mul", "sub"])
            val = self._rng.randint(1, 5)
            if op == "add":
                x += val
                ops.append(f"x = x + {val}")
            elif op == "mul":
                x *= val
                ops.append(f"x = x * {val}")
            else:
                x -= val
                ops.append(f"x = x - {val}")
            steps.append(f"x = {x}")

        program = f"x = {init}; " + "; ".join(ops) + "; return x"
        return program, {"steps": steps, "answer": x}

    def _swap_program(self, difficulty: int) -> tuple[str, dict]:
        """Generate a variable swap program.

        Args:
            difficulty: Controls number of swaps.

        Returns:
            Tuple of (program_text, solution_data).
        """
        a = self._rng.randint(1, 10)
        b = self._rng.randint(1, 10)
        num_swaps = min(1 + difficulty // 2, 4)

        steps = [f"a={a}, b={b}"]
        program_parts = [f"a={a}; b={b}"]

        for i in range(num_swaps):
            a, b = b, a
            steps.append(f"swap: a={a}, b={b}")
            program_parts.append("swap(a,b)")

        op = self._rng.choice(["add", "sub"])
        if op == "add":
            result = a + b
            program_parts.append("return a+b")
            steps.append(f"a+b = {a}+{b} = {result}")
        else:
            result = a - b
            program_parts.append("return a-b")
            steps.append(f"a-b = {a}-{b} = {result}")

        program = "; ".join(program_parts)
        return program, {"steps": steps, "answer": result}

    def _conditional_program(self, difficulty: int) -> tuple[str, dict]:
        """Generate a conditional branch program.

        Args:
            difficulty: Controls nesting depth.

        Returns:
            Tuple of (program_text, solution_data).
        """
        x = self._rng.randint(-5, 10)
        threshold = self._rng.randint(0, 5)
        a_val = self._rng.randint(1, 10)
        b_val = self._rng.randint(1, 10)

        if x > threshold:
            result = x + a_val
            branch = "if-branch"
            steps = [f"x={x}, x>{threshold} is True", f"x = {x} + {a_val} = {result}"]
        else:
            result = x * b_val
            branch = "else-branch"
            steps = [f"x={x}, x>{threshold} is False", f"x = {x} * {b_val} = {result}"]

        program = f"x={x}; if x>{threshold}: x=x+{a_val}; else: x=x*{b_val}; return x"
        return program, {"steps": steps, "answer": result, "branch": branch}

    def _create_steps(self, solution_data: dict) -> list[str]:
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        return str(solution_data["answer"])


@register_oos
class MusicalIntervalGenerator(StepGenerator):
    """Musical interval arithmetic with octave wrapping.

    Shares structure with: modular arithmetic, base conversion.
    Requires: modular reasoning in an unfamiliar domain.
    """

    _NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    _INTERVAL_NAMES = {
        0: "unison", 1: "minor 2nd", 2: "major 2nd", 3: "minor 3rd",
        4: "major 3rd", 5: "perfect 4th", 6: "tritone", 7: "perfect 5th",
        8: "minor 6th", 9: "major 6th", 10: "minor 7th", 11: "major 7th",
        12: "octave",
    }

    @property
    def task_name(self) -> str:
        return "oos_musical_interval"

    @property
    def tier(self) -> int:
        return 99

    def task_description(self, difficulty: int) -> str:
        return "compute musical interval"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a musical interval problem.

        Args:
            difficulty: Controls number of intervals to chain.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        start_idx = self._rng.randint(0, 11)
        start_note = self._NOTES[start_idx]
        num_intervals = min(1 + difficulty // 2, 5)

        intervals = []
        steps = []
        current_idx = start_idx

        for _ in range(num_intervals):
            semitones = self._rng.randint(1, 12)
            direction = self._rng.choice(["up", "down"])

            if direction == "up":
                new_idx = (current_idx + semitones) % 12
                dir_symbol = "+"
            else:
                new_idx = (current_idx - semitones) % 12
                dir_symbol = "-"

            interval_name = self._INTERVAL_NAMES.get(semitones, f"{semitones} semitones")
            old_note = self._NOTES[current_idx]
            new_note = self._NOTES[new_idx]
            steps.append(f"{old_note} {dir_symbol} {interval_name} ({semitones}st) = {new_note}")
            intervals.append((direction, semitones))
            current_idx = new_idx

        interval_strs = []
        for direction, semitones in intervals:
            name = self._INTERVAL_NAMES.get(semitones, f"{semitones}st")
            interval_strs.append(f"{direction} {name}")

        problem = f"{start_note} -> {' -> '.join(interval_strs)}"
        final_note = self._NOTES[current_idx]

        return problem, {
            "steps": steps,
            "answer": final_note,
            "start": start_note,
            "intervals": intervals,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        return solution_data["answer"]
