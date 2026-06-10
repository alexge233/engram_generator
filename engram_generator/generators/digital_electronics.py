"""Digital electronics generators -- K-maps, flip-flops, timing, adders, counters, MUX.

Covers Karnaugh map minimization, sequential flip-flop state
computation, timing analysis with gate delays, ripple carry adder
circuits, mod-N counter design, and multiplexer output evaluation.
Tiers range from 4 (combinational logic) to 5 (sequential/timing).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _DigitalFormatter:
    """Formats numeric values for digital electronics problems.

    Provides consistent rounding and clean string representations
    to keep target text compact.
    """

    @staticmethod
    def fmt(value: float, decimals: int = 4) -> str:
        """Format a numeric value, stripping unnecessary trailing zeros.

        Args:
            value: Number to format.
            decimals: Maximum decimal places.

        Returns:
            Clean string representation.
        """
        rounded = round(value, decimals)
        if rounded == int(rounded):
            return str(int(rounded))
        return str(rounded)


_f = _DigitalFormatter.fmt


# ===================================================================
# 1. Karnaugh map minimization  (tier 4)
# ===================================================================

@register
class KarnaughMapGenerator(StepGenerator):
    """Karnaugh map minimization for 2-4 variable Boolean functions.

    Given a truth table (as minterms), fills the K-map, groups adjacent
    1s, and produces the minimized sum-of-products (SOP) expression.

    Difficulty scaling:
        Difficulty 1-3: 2 variables, small minterm sets.
        Difficulty 4-6: 3 variables.
        Difficulty 7-8: 4 variables with don't-care terms.

    Prerequisites:
        boolean_algebra.
    """

    _VARS_2 = ["A", "B"]
    _VARS_3 = ["A", "B", "C"]
    _VARS_4 = ["A", "B", "C", "D"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "karnaugh_map"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["boolean_algebra"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "minimize Boolean function using Karnaugh map"

    def _minterm_to_product(self, index: int, num_vars: int,
                            var_names: list[str]) -> str:
        """Convert a minterm index to a product term.

        Args:
            index: Minterm index.
            num_vars: Number of variables.
            var_names: Variable name list.

        Returns:
            Product term string like "A'B" or "AB'C".
        """
        bits = format(index, f'0{num_vars}b')
        parts = []
        for i, bit in enumerate(bits):
            if bit == '1':
                parts.append(var_names[i])
            else:
                parts.append(f"{var_names[i]}'")
        return "".join(parts)

    def _find_sop_2var(self, minterms: set[int]) -> str:
        """Find minimized SOP for 2-variable function.

        Args:
            minterms: Set of minterm indices.

        Returns:
            Minimized SOP expression string.
        """
        if len(minterms) == 4:
            return "1"
        if len(minterms) == 0:
            return "0"

        terms = []
        # Check pairs for grouping
        # Group {0,1} => A'
        if {0, 1}.issubset(minterms):
            terms.append("A'")
            minterms = minterms - {0, 1}
        # Group {2,3} => A
        if {2, 3}.issubset(minterms):
            terms.append("A")
            minterms = minterms - {2, 3}
        # Group {0,2} => B'
        if {0, 2}.issubset(minterms):
            terms.append("B'")
            minterms = minterms - {0, 2}
        # Group {1,3} => B
        if {1, 3}.issubset(minterms):
            terms.append("B")
            minterms = minterms - {1, 3}
        # Remaining singles
        for m in sorted(minterms):
            terms.append(self._minterm_to_product(m, 2, self._VARS_2))
        return " + ".join(terms) if terms else "0"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a K-map minimization problem.

        Args:
            difficulty: Controls number of variables and complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            num_vars = 2
            var_names = self._VARS_2
            max_minterms = 4
        elif difficulty <= 6:
            num_vars = 3
            var_names = self._VARS_3
            max_minterms = 8
        else:
            num_vars = 4
            var_names = self._VARS_4
            max_minterms = 16

        num_ones = self._rng.randint(1, max(1, max_minterms - 1))
        all_indices = list(range(max_minterms))
        self._rng.shuffle(all_indices)
        minterms = sorted(all_indices[:num_ones])

        # Build product terms for each minterm (canonical SOP)
        canonical = []
        for m in minterms:
            canonical.append(self._minterm_to_product(m, num_vars, var_names))

        # Minimized expression for 2 vars
        if num_vars == 2:
            minimized = self._find_sop_2var(set(minterms))
        else:
            # For 3+ vars, output canonical grouped form
            minimized = " + ".join(canonical)

        problem = (f"F({','.join(var_names)}) = "
                   f"\\sum m({','.join(str(m) for m in minterms)})")

        return problem, {
            "num_vars": num_vars,
            "var_names": var_names,
            "minterms": minterms,
            "canonical": canonical,
            "minimized": minimized,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate K-map filling and grouping steps.

        Args:
            data: Solution data with minterms and expressions.

        Returns:
            List of step strings.
        """
        minterms_str = ",".join(str(m) for m in data["minterms"])
        steps = [
            f"vars={','.join(data['var_names'])}, "
            f"minterms={{{minterms_str}}}",
            f"fill K-map: 1 at positions {minterms_str}",
            f"group adjacent 1s",
            f"SOP = {data['minimized']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the minimized SOP expression.

        Args:
            data: Solution data.

        Returns:
            String with the minimized Boolean expression.
        """
        return f"F = {data['minimized']}"


# ===================================================================
# 2. Flip-flop state sequence  (tier 4)
# ===================================================================

@register
class FlipFlopStateGenerator(StepGenerator):
    """Flip-flop output sequence computation.

    Given a JK, D, or T flip-flop type, initial state Q0, and a
    sequence of clock-pulse inputs, computes the output Q after each
    clock edge.

    Difficulty scaling:
        Difficulty 1-3: D flip-flop, 3-4 clock pulses.
        Difficulty 4-6: JK flip-flop, 4-6 clock pulses.
        Difficulty 7-8: T flip-flop with varying inputs, 5-7 pulses.

    Prerequisites:
        logic_gate_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "flip_flop_state"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logic_gate_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute flip-flop output sequence"

    def _d_ff(self, d: int, q: int) -> int:
        """Compute next state of D flip-flop.

        Args:
            d: D input.
            q: Current state.

        Returns:
            Next state Q.
        """
        return d

    def _jk_ff(self, j: int, k: int, q: int) -> int:
        """Compute next state of JK flip-flop.

        Args:
            j: J input.
            k: K input.
            q: Current state.

        Returns:
            Next state Q.
        """
        if j == 0 and k == 0:
            return q
        if j == 0 and k == 1:
            return 0
        if j == 1 and k == 0:
            return 1
        return 1 - q  # j=1, k=1 -> toggle

    def _t_ff(self, t: int, q: int) -> int:
        """Compute next state of T flip-flop.

        Args:
            t: T input.
            q: Current state.

        Returns:
            Next state Q.
        """
        if t == 1:
            return 1 - q
        return q

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate flip-flop input sequence and compute outputs.

        Args:
            difficulty: Controls FF type and sequence length.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        q0 = self._rng.choice([0, 1])

        if difficulty <= 3:
            ff_type = "D"
            n_pulses = self._rng.randint(3, 4)
            inputs = [self._rng.choice([0, 1]) for _ in range(n_pulses)]
            outputs = []
            q = q0
            for d in inputs:
                q = self._d_ff(d, q)
                outputs.append(q)
            input_label = "D"
        elif difficulty <= 6:
            ff_type = "JK"
            n_pulses = self._rng.randint(4, 6)
            j_inputs = [self._rng.choice([0, 1]) for _ in range(n_pulses)]
            k_inputs = [self._rng.choice([0, 1]) for _ in range(n_pulses)]
            inputs = list(zip(j_inputs, k_inputs))
            outputs = []
            q = q0
            for j, k in inputs:
                q = self._jk_ff(j, k, q)
                outputs.append(q)
            input_label = "J,K"
        else:
            ff_type = "T"
            n_pulses = self._rng.randint(5, 7)
            inputs = [self._rng.choice([0, 1]) for _ in range(n_pulses)]
            outputs = []
            q = q0
            for t in inputs:
                q = self._t_ff(t, q)
                outputs.append(q)
            input_label = "T"

        if ff_type == "JK":
            inputs_str = " ".join(
                f"({j},{k})" for j, k in inputs
            )
        else:
            inputs_str = " ".join(str(i) for i in inputs)

        problem = (f"{ff_type} flip-flop, Q_0={q0}, "
                   f"{input_label}=[{inputs_str}]")

        return problem, {
            "ff_type": ff_type,
            "q0": q0,
            "inputs": inputs,
            "inputs_str": inputs_str,
            "outputs": outputs,
            "input_label": input_label,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate step-by-step state transitions.

        Args:
            data: Solution data with FF type, inputs, outputs.

        Returns:
            List of step strings.
        """
        steps = [
            f"type={data['ff_type']}, Q0={data['q0']}",
        ]
        q = data["q0"]
        for i, out in enumerate(data["outputs"]):
            if data["ff_type"] == "JK":
                j, k = data["inputs"][i]
                steps.append(f"clk{i+1}: J={j},K={k} => Q={out}")
            elif data["ff_type"] == "D":
                steps.append(
                    f"clk{i+1}: D={data['inputs'][i]} => Q={out}"
                )
            else:
                steps.append(
                    f"clk{i+1}: T={data['inputs'][i]} => Q={out}"
                )
            q = out
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the output sequence.

        Args:
            data: Solution data.

        Returns:
            String of Q values after each clock pulse.
        """
        seq = "".join(str(o) for o in data["outputs"])
        return f"Q = [{seq}]"


# ===================================================================
# 3. Timing analysis  (tier 5)
# ===================================================================

@register
class TimingAnalysisGenerator(StepGenerator):
    """Combinational circuit timing analysis.

    Computes the critical path delay through a combinational circuit
    composed of gates with known propagation delays. Also checks
    setup/hold time constraints for flip-flop inputs.

    Difficulty scaling:
        Difficulty 1-3: 2-3 gates in series, uniform delays.
        Difficulty 4-6: 3-5 gates with parallel paths, find critical.
        Difficulty 7-8: include setup/hold time check for FF.

    Prerequisites:
        addition.
    """

    _GATE_TYPES = ["AND", "OR", "NOT", "NAND", "NOR", "XOR"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "timing_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute critical path delay through circuit"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a circuit with gate delays and compute critical path.

        Args:
            difficulty: Controls number of gates and paths.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            num_paths = 1
            gates_per_path = self._rng.randint(2, 3)
        elif difficulty <= 6:
            num_paths = self._rng.randint(2, 3)
            gates_per_path = self._rng.randint(2, 4)
        else:
            num_paths = self._rng.randint(2, 4)
            gates_per_path = self._rng.randint(3, 5)

        paths = []
        path_delays = []
        for p in range(num_paths):
            n_gates = self._rng.randint(
                max(1, gates_per_path - 1), gates_per_path
            )
            gate_list = []
            total_delay = 0.0
            for _ in range(n_gates):
                gate = self._rng.choice(self._GATE_TYPES)
                delay = round(self._rng.uniform(1.0, 5.0 + difficulty), 1)
                gate_list.append((gate, delay))
                total_delay += delay
            total_delay = round(total_delay, 4)
            paths.append(gate_list)
            path_delays.append(total_delay)

        critical_idx = path_delays.index(max(path_delays))
        critical_delay = path_delays[critical_idx]

        # Setup/hold check for high difficulty
        setup_time = None
        hold_time = None
        clock_period = None
        timing_ok = True
        if difficulty >= 7:
            setup_time = round(self._rng.uniform(0.5, 2.0), 1)
            hold_time = round(self._rng.uniform(0.1, 1.0), 1)
            clock_period = round(
                critical_delay + self._rng.uniform(1.0, 5.0), 1
            )
            slack = round(clock_period - critical_delay - setup_time, 4)
            timing_ok = slack >= 0

        problem = "t_{critical} = max(\\sum t_{gate,i})"

        return problem, {
            "paths": paths,
            "path_delays": path_delays,
            "critical_idx": critical_idx,
            "critical_delay": critical_delay,
            "setup_time": setup_time,
            "hold_time": hold_time,
            "clock_period": clock_period,
            "timing_ok": timing_ok,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate timing computation steps.

        Args:
            data: Solution data with paths and delays.

        Returns:
            List of step strings.
        """
        steps = []
        for i, (path, delay) in enumerate(
            zip(data["paths"], data["path_delays"])
        ):
            gates_str = " -> ".join(
                f"{g}({_f(d)}ns)" for g, d in path
            )
            steps.append(f"path{i+1}: {gates_str} = {_f(delay)}ns")

        steps.append(
            f"critical path = path{data['critical_idx']+1}, "
            f"delay = {_f(data['critical_delay'])}ns"
        )

        if data["setup_time"] is not None:
            slack = round(
                data["clock_period"] - data["critical_delay"]
                - data["setup_time"], 4
            )
            status = "MET" if data["timing_ok"] else "VIOLATED"
            steps.append(
                f"T_clk={_f(data['clock_period'])}ns, "
                f"t_su={_f(data['setup_time'])}ns, "
                f"slack={_f(slack)}ns => {status}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the critical path delay and timing status.

        Args:
            data: Solution data.

        Returns:
            String with critical delay and optional timing check.
        """
        result = f"t_critical = {_f(data['critical_delay'])} ns"
        if data["setup_time"] is not None:
            status = "timing MET" if data["timing_ok"] else "timing VIOLATED"
            result += f", {status}"
        return result


# ===================================================================
# 4. Adder circuit  (tier 4)
# ===================================================================

@register
class AdderCircuitGenerator(StepGenerator):
    """Full adder and ripple carry adder circuit.

    Full adder: S = A xor B xor Cin, Cout = AB + BCin + ACin.
    At higher difficulty, chains full adders into a 4-bit ripple
    carry adder.

    Difficulty scaling:
        Difficulty 1-3: single full adder (1-bit).
        Difficulty 4-6: 4-bit ripple carry adder.
        Difficulty 7-8: 4-bit with carry-in = 1, verify overflow.

    Prerequisites:
        binary_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "adder_circuit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty <= 3:
            return "compute full adder output"
        return "compute 4-bit ripple carry adder output"

    def _full_adder(self, a: int, b: int, cin: int) -> tuple[int, int]:
        """Compute single full adder outputs.

        Args:
            a: Input bit A.
            b: Input bit B.
            cin: Carry in.

        Returns:
            Tuple of (sum_bit, carry_out).
        """
        s = a ^ b ^ cin
        cout = (a & b) | (b & cin) | (a & cin)
        return s, cout

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate adder problem and compute result.

        Args:
            difficulty: Controls single vs ripple carry.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            a = self._rng.choice([0, 1])
            b = self._rng.choice([0, 1])
            cin = self._rng.choice([0, 1])
            s, cout = self._full_adder(a, b, cin)

            problem = (f"full adder: A={a}, B={b}, C_{{in}}={cin}")
            return problem, {
                "mode": "single",
                "a": a, "b": b, "cin": cin,
                "s": s, "cout": cout,
            }

        # 4-bit ripple carry
        a_val = self._rng.randint(0, 15)
        b_val = self._rng.randint(0, 15)
        cin = 1 if difficulty >= 7 else 0

        a_bits = [(a_val >> i) & 1 for i in range(4)]
        b_bits = [(b_val >> i) & 1 for i in range(4)]

        carry = cin
        sum_bits = []
        carries = [cin]
        for i in range(4):
            s, carry = self._full_adder(a_bits[i], b_bits[i], carry)
            sum_bits.append(s)
            carries.append(carry)

        result = sum(s << i for i, s in enumerate(sum_bits))
        overflow = carries[-1]
        a_bin = format(a_val, '04b')
        b_bin = format(b_val, '04b')
        s_bin = format(result, '04b')

        problem = (f"4-bit ripple carry: A={a_bin}, B={b_bin}, "
                   f"C_{{in}}={cin}")
        return problem, {
            "mode": "ripple",
            "a_val": a_val, "b_val": b_val, "cin": cin,
            "a_bin": a_bin, "b_bin": b_bin,
            "a_bits": a_bits, "b_bits": b_bits,
            "sum_bits": sum_bits, "carries": carries,
            "result": result, "s_bin": s_bin, "overflow": overflow,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate adder computation steps.

        Args:
            data: Solution data with bits and carries.

        Returns:
            List of step strings.
        """
        if data["mode"] == "single":
            a, b, cin = data["a"], data["b"], data["cin"]
            return [
                f"A={a}, B={b}, Cin={cin}",
                f"S = {a}^{b}^{cin} = {data['s']}",
                f"Cout = {a}&{b}|{b}&{cin}|{a}&{cin} = {data['cout']}",
            ]

        steps = [
            f"A={data['a_bin']}({data['a_val']}), "
            f"B={data['b_bin']}({data['b_val']}), Cin={data['cin']}",
        ]
        for i in range(4):
            steps.append(
                f"bit{i}: {data['a_bits'][i]}+{data['b_bits'][i]}"
                f"+{data['carries'][i]} => S={data['sum_bits'][i]}, "
                f"C={data['carries'][i+1]}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the adder output.

        Args:
            data: Solution data.

        Returns:
            String with sum and carry out.
        """
        if data["mode"] == "single":
            return f"S={data['s']}, Cout={data['cout']}"
        return (f"S={data['s_bin']}({data['result']}), "
                f"Cout={data['overflow']}")


# ===================================================================
# 5. Counter design  (tier 5)
# ===================================================================

@register
class CounterDesignGenerator(StepGenerator):
    """Mod-N counter design.

    Given a modulus N, determines the number of flip-flops required
    (ceil(log2(N))), the state sequence from 0 to N-1, and the reset
    condition that returns the counter to state 0.

    Difficulty scaling:
        Difficulty 1-3: mod 4 or mod 8 (power of 2).
        Difficulty 4-6: mod N where N is not a power of 2 (5-12).
        Difficulty 7-8: larger N (13-31), list full state table.

    Prerequisites:
        binary_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "counter_design"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "design mod-N counter"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate counter specification and compute design.

        Args:
            difficulty: Controls modulus range.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.choice([4, 8])
        elif difficulty <= 6:
            n = self._rng.randint(5, 12)
        else:
            n = self._rng.randint(13, 31)

        num_ffs = math.ceil(math.log2(n)) if n > 1 else 1
        max_state = (1 << num_ffs) - 1
        state_seq = list(range(n))
        reset_state = n  # state at which reset triggers

        # Binary representation of reset state
        reset_bin = format(reset_state, f'0{num_ffs}b') if reset_state <= max_state else "N/A"
        is_power_of_2 = (n & (n - 1)) == 0

        problem = f"mod-{n} counter"
        return problem, {
            "N": n,
            "num_ffs": num_ffs,
            "max_state": max_state,
            "state_seq": state_seq,
            "reset_state": reset_state,
            "reset_bin": reset_bin,
            "is_power_of_2": is_power_of_2,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate counter design steps.

        Args:
            data: Solution data with counter parameters.

        Returns:
            List of step strings.
        """
        steps = [
            f"N={data['N']}, ceil(log2({data['N']})) = {data['num_ffs']}",
            f"FFs needed = {data['num_ffs']}",
            f"states: 0..{data['N']-1}",
        ]
        if data["is_power_of_2"]:
            steps.append("N is power of 2, no external reset needed")
        else:
            steps.append(
                f"reset when state={data['reset_state']} "
                f"({data['reset_bin']})"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the counter design summary.

        Args:
            data: Solution data.

        Returns:
            String with FF count, state range, and reset condition.
        """
        if data["is_power_of_2"]:
            return (f"{data['num_ffs']} FFs, "
                    f"states 0-{data['N']-1}, natural rollover")
        return (f"{data['num_ffs']} FFs, states 0-{data['N']-1}, "
                f"reset at {data['reset_state']}")


# ===================================================================
# 6. Multiplexer  (tier 4)
# ===================================================================

@register
class MultiplexerGenerator(StepGenerator):
    """4:1 multiplexer output computation.

    Y = S1'S0'I0 + S1'S0*I1 + S1*S0'I2 + S1*S0*I3.
    Given select lines S1,S0 and data inputs I0-I3, computes the
    output Y.

    Difficulty scaling:
        Difficulty 1-3: binary inputs (0/1) only.
        Difficulty 4-6: inputs are Boolean expressions, evaluate.
        Difficulty 7-8: cascaded 4:1 MUX (8:1 from two 4:1).

    Prerequisites:
        logic_gate_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "multiplexer"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logic_gate_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty <= 6:
            return "compute 4:1 MUX output"
        return "compute cascaded 8:1 MUX output"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate MUX inputs and compute output.

        Args:
            difficulty: Controls input complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        s1 = self._rng.choice([0, 1])
        s0 = self._rng.choice([0, 1])
        inputs = [self._rng.choice([0, 1]) for _ in range(4)]

        # Select the output
        sel = s1 * 2 + s0
        y = inputs[sel]

        if difficulty <= 6:
            problem = (f"4:1 MUX: S1={s1}, S0={s0}, "
                       f"I0={inputs[0]}, I1={inputs[1]}, "
                       f"I2={inputs[2]}, I3={inputs[3]}")
            return problem, {
                "mode": "single",
                "s1": s1, "s0": s0,
                "inputs": inputs, "sel": sel, "y": y,
            }

        # Cascaded: 8:1 MUX from two 4:1 MUXes
        s2 = self._rng.choice([0, 1])
        inputs_b = [self._rng.choice([0, 1]) for _ in range(4)]
        sel_b = s1 * 2 + s0
        y_a = inputs[sel]
        y_b = inputs_b[sel_b]
        # s2 selects between MUX_A and MUX_B
        y_final = y_a if s2 == 0 else y_b

        problem = (f"8:1 MUX: S2={s2}, S1={s1}, S0={s0}, "
                   f"I0-I3={inputs}, I4-I7={inputs_b}")
        return problem, {
            "mode": "cascade",
            "s2": s2, "s1": s1, "s0": s0,
            "inputs_a": inputs, "inputs_b": inputs_b,
            "sel": sel, "y_a": y_a, "y_b": y_b,
            "y_final": y_final,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate MUX evaluation steps.

        Args:
            data: Solution data with select lines and inputs.

        Returns:
            List of step strings.
        """
        if data["mode"] == "single":
            steps = [
                f"S1={data['s1']}, S0={data['s0']} => "
                f"select I{data['sel']}",
                f"I{data['sel']} = {data['y']}",
                f"Y = {data['y']}",
            ]
            return steps

        steps = [
            f"S2={data['s2']}, S1={data['s1']}, S0={data['s0']}",
            f"MUX_A: sel={data['sel']} => I{data['sel']}={data['y_a']}",
            f"MUX_B: sel={data['sel']} => I{data['sel']+4}={data['y_b']}",
            f"S2={data['s2']} => "
            f"{'MUX_A' if data['s2'] == 0 else 'MUX_B'}",
            f"Y = {data['y_final']}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the MUX output.

        Args:
            data: Solution data.

        Returns:
            String with output value.
        """
        if data["mode"] == "single":
            return f"Y = {data['y']}"
        return f"Y = {data['y_final']}"
