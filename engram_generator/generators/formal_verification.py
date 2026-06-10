"""Formal verification generators.

8 generators across tiers 6-7 covering Hoare logic, weakest preconditions,
loop invariants, CTL model checking, LTL-to-Buchi conversion,
bisimulation, CEGAR abstraction refinement, and invariant synthesis.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# 1. HOARE TRIPLE (tier 6)
# ===================================================================

@register
class HoareTripleGenerator(StepGenerator):
    """Verify Hoare triples {P} S {Q} for simple programs.

    Given a precondition P, a statement S (assignment, conditional),
    and a postcondition Q, determine whether {P} S {Q} holds.

    Difficulty scaling:
        Difficulty 1-3: single assignment.
        Difficulty 4-6: two sequential assignments.
        Difficulty 7-8: conditional statement.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hoare_triple"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["propositional_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "verify Hoare triple {P} S {Q}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hoare triple verification problem.

        Args:
            difficulty: Controls statement complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        var = self._rng.choice(["x", "y", "z", "n", "m"])
        a = self._rng.randint(0, 10)
        b = self._rng.randint(1, 8)

        if difficulty <= 3:
            # Single assignment: {var=a} var:=var+b {var=a+b}
            pre = f"{var}={a}"
            stmt = f"{var}:={var}+{b}"
            post_val = a + b
            post = f"{var}={post_val}"
            valid = True
            wp = f"{var}+{b}={post_val} => {var}={a}"
            steps_detail = [
                f"wp({var}:={var}+{b}, {var}={post_val})"
                f" = {var}+{b}={post_val} = ({var}={a})",
                f"precondition {var}={a} implies wp: {valid}",
            ]
        elif difficulty <= 6:
            # Two assignments: {var=a} var:=var+b; var:=var*2 {var=2*(a+b)}
            c = 2
            pre = f"{var}={a}"
            stmt = f"{var}:={var}+{b}; {var}:={var}*{c}"
            post_val = c * (a + b)
            post = f"{var}={post_val}"
            valid = True
            wp = (f"wp({var}:={var}*{c}, {var}={post_val})"
                  f" = {var}*{c}={post_val} = ({var}={a + b})")
            steps_detail = [
                wp,
                f"wp({var}:={var}+{b}, {var}={a + b})"
                f" = {var}+{b}={a + b} = ({var}={a})",
                f"precondition {var}={a} implies wp: {valid}",
            ]
        else:
            # Conditional: {var>=0} if var>0 then var:=var-1 else var:=var+1 {var>=0}
            pre = f"{var}>=0"
            stmt = (f"if {var}>0 then {var}:={var}-1"
                    f" else {var}:={var}+1")
            post = f"{var}>=0"
            valid = True
            steps_detail = [
                f"branch {var}>0: wp({var}:={var}-1, {var}>=0)"
                f" = {var}-1>=0 = ({var}>=1)",
                f"{var}>0 implies {var}>=1: True",
                f"branch {var}<=0 and {var}>=0: {var}=0",
                f"wp({var}:={var}+1, {var}>=0) = {var}+1>=0: True",
                f"both branches valid: {valid}",
            ]

        # Occasionally make it invalid for higher difficulty
        if difficulty >= 4 and self._rng.random() < 0.3:
            wrong_val = self._rng.randint(0, 20)
            post = f"{var}={wrong_val}"
            valid = False
            steps_detail.append(f"postcondition {post} does NOT follow")

        problem = "{" + pre + "} " + stmt + " {" + post + "}"
        return problem, {
            "pre": pre, "stmt": stmt, "post": post,
            "valid": valid, "steps_detail": steps_detail,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps_detail"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            VALID or INVALID.
        """
        return "VALID" if sd["valid"] else "INVALID"


# ===================================================================
# 2. WEAKEST PRECONDITION CALCULUS (tier 6)
# ===================================================================

@register
class WPCalculusGenerator(StepGenerator):
    """Compute weakest precondition for assignment chains.

    wp(x:=E, Q) = Q[x/E]. Chains computed right to left.

    Difficulty scaling:
        Difficulty 1-3: single assignment.
        Difficulty 4-6: two sequential assignments.
        Difficulty 7-8: three sequential assignments.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wp_calculus"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hoare_triple"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute weakest precondition for assignment chain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a weakest precondition problem.

        Args:
            difficulty: Controls number of assignments.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        var = self._rng.choice(["x", "y", "z"])
        ops = ["+", "-", "*"]

        if difficulty <= 3:
            n_stmts = 1
        elif difficulty <= 6:
            n_stmts = 2
        else:
            n_stmts = 3

        # Build assignment chain
        assignments = []
        constants = []
        for _ in range(n_stmts):
            op = self._rng.choice(ops[:min(len(ops), 1 + difficulty // 2)])
            c = self._rng.randint(1, 5)
            assignments.append(f"{var}:={var}{op}{c}")
            constants.append((op, c))

        # Postcondition: var = target
        target = self._rng.randint(1, 20)
        postcond = f"{var}={target}"

        # Compute wp right to left
        steps = []
        current_target = target
        for i in range(n_stmts - 1, -1, -1):
            op, c = constants[i]
            stmt = assignments[i]
            # wp(var:=var op c, var=current) => var op c = current => var = inverse
            if op == "+":
                new_target = current_target - c
                sub_expr = f"{var}+{c}={current_target} => {var}={new_target}"
            elif op == "-":
                new_target = current_target + c
                sub_expr = f"{var}-{c}={current_target} => {var}={new_target}"
            else:  # *
                if current_target % c == 0:
                    new_target = current_target // c
                else:
                    new_target = current_target / c
                sub_expr = (f"{var}*{c}={current_target}"
                            f" => {var}={new_target}")
            steps.append(f"wp({stmt}, {var}={current_target}): {sub_expr}")
            current_target = new_target

        wp_result = f"{var}={current_target}"
        stmt_chain = "; ".join(assignments)
        problem = f"wp({stmt_chain}, {postcond})"

        return problem, {
            "assignments": assignments,
            "postcond": postcond,
            "steps_detail": steps,
            "wp": wp_result,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps_detail"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Weakest precondition as a string.
        """
        return sd["wp"]


# ===================================================================
# 3. LOOP INVARIANT VERIFICATION (tier 7)
# ===================================================================

@register
class LoopInvariantVerifyGenerator(StepGenerator):
    """Verify a proposed loop invariant.

    Check three conditions:
    1. P => I (initiation)
    2. {I AND B} body {I} (consecution)
    3. I AND NOT B => Q (termination)

    Difficulty scaling:
        Difficulty 1-4: summation loop.
        Difficulty 5-8: multiplication/factorial loop.
    """

    _LOOP_TEMPLATES = [
        {
            "name": "summation",
            "var": "s", "idx": "i", "bound_var": "n",
            "init": "s:=0; i:=0",
            "guard": "i<n",
            "body": "s:=s+i; i:=i+1",
            "invariant": "s = i*(i-1)/2 AND i<=n",
            "postcond": "s = n*(n-1)/2",
        },
        {
            "name": "factorial",
            "var": "f", "idx": "i", "bound_var": "n",
            "init": "f:=1; i:=1",
            "guard": "i<=n",
            "body": "f:=f*i; i:=i+1",
            "invariant": "f = (i-1)! AND i<=n+1",
            "postcond": "f = n!",
        },
        {
            "name": "power",
            "var": "p", "idx": "i", "bound_var": "n",
            "init": "p:=1; i:=0",
            "guard": "i<n",
            "body": "p:=p*b; i:=i+1",
            "invariant": "p = b^i AND i<=n",
            "postcond": "p = b^n",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "loop_invariant_verify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hoare_triple"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "verify loop invariant for all three conditions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a loop invariant verification problem.

        Args:
            difficulty: Controls loop template complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            template = self._LOOP_TEMPLATES[0]
        else:
            template = self._rng.choice(self._LOOP_TEMPLATES[1:])

        n_val = self._rng.randint(3, 6 + difficulty)
        valid = True

        # Occasionally propose a wrong invariant
        if self._rng.random() < 0.25:
            wrong_inv = template["invariant"].replace("<=", "<")
            invariant = wrong_inv
            valid = False
        else:
            invariant = template["invariant"]

        problem = (
            f"init: {template['init']}; "
            f"while {template['guard']} do {template['body']}; "
            f"I: {invariant}; Q: {template['postcond']}; "
            f"{template['bound_var']}={n_val}"
        )

        steps = [
            f"1. Initiation: after init, check I holds",
            f"   {template['init']} => {invariant}: {'True' if valid else 'check needed'}",
            f"2. Consecution: {{I AND {template['guard']}}} {template['body']} {{I}}",
            f"   assume I and {template['guard']}, execute body, verify I",
            f"3. Termination: I AND NOT({template['guard']}) => {template['postcond']}",
        ]
        if valid:
            steps.append("all three conditions hold => invariant valid")
        else:
            steps.append("invariant violation detected => INVALID")

        return problem, {
            "template": template["name"],
            "invariant": invariant,
            "postcond": template["postcond"],
            "valid": valid,
            "steps_detail": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps_detail"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            VALID or INVALID.
        """
        return "VALID" if sd["valid"] else "INVALID"


# ===================================================================
# 4. CTL MODEL CHECKING (tier 7)
# ===================================================================

@register
class CTLModelCheckGenerator(StepGenerator):
    """Evaluate CTL formula on a finite Kripke structure.

    Supports EX, AX, EF, AG, and EU operators on small
    transition systems with labeled states.

    Difficulty scaling:
        Difficulty 1-3: 3 states, EX/AX.
        Difficulty 4-6: 4 states, EF/AG.
        Difficulty 7-8: 5 states, EU.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ctl_model_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["temporal_logic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "evaluate CTL formula on Kripke structure"

    def _build_kripke(self, n: int) -> tuple[dict, dict]:
        """Build a random Kripke structure with n states.

        Args:
            n: Number of states.

        Returns:
            Tuple of (transitions, labels).
        """
        states = [f"s{i}" for i in range(n)]
        props = ["p", "q", "r"]

        labels = {}
        for s in states:
            assigned = [pr for pr in props if self._rng.random() < 0.5]
            labels[s] = set(assigned)

        transitions = {}
        for s in states:
            n_succ = self._rng.randint(1, min(3, n))
            succs = self._rng.sample(states, n_succ)
            transitions[s] = succs

        return transitions, labels

    def _eval_ex(self, state: str, prop: str, trans: dict,
                 labels: dict) -> bool:
        """Evaluate EX prop at state.

        Args:
            state: Current state.
            prop: Atomic proposition.
            trans: Transition relation.
            labels: State labeling.

        Returns:
            True if EX prop holds at state.
        """
        return any(prop in labels.get(s, set()) for s in trans.get(state, []))

    def _eval_ax(self, state: str, prop: str, trans: dict,
                 labels: dict) -> bool:
        """Evaluate AX prop at state.

        Args:
            state: Current state.
            prop: Atomic proposition.
            trans: Transition relation.
            labels: State labeling.

        Returns:
            True if AX prop holds at state.
        """
        successors = trans.get(state, [])
        if not successors:
            return True
        return all(prop in labels.get(s, set()) for s in successors)

    def _eval_ef(self, state: str, prop: str, trans: dict,
                 labels: dict) -> bool:
        """Evaluate EF prop at state via BFS.

        Args:
            state: Current state.
            prop: Atomic proposition.
            trans: Transition relation.
            labels: State labeling.

        Returns:
            True if EF prop holds at state.
        """
        visited = set()
        queue = [state]
        while queue:
            s = queue.pop(0)
            if s in visited:
                continue
            visited.add(s)
            if prop in labels.get(s, set()):
                return True
            queue.extend(trans.get(s, []))
        return False

    def _eval_ag(self, state: str, prop: str, trans: dict,
                 labels: dict) -> bool:
        """Evaluate AG prop at state via BFS.

        Args:
            state: Current state.
            prop: Atomic proposition.
            trans: Transition relation.
            labels: State labeling.

        Returns:
            True if AG prop holds at state.
        """
        visited = set()
        queue = [state]
        while queue:
            s = queue.pop(0)
            if s in visited:
                continue
            visited.add(s)
            if prop not in labels.get(s, set()):
                return False
            queue.extend(trans.get(s, []))
        return True

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CTL model checking problem.

        Args:
            difficulty: Controls Kripke structure size and operator.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 3
            op = self._rng.choice(["EX", "AX"])
        elif difficulty <= 6:
            n = 4
            op = self._rng.choice(["EF", "AG"])
        else:
            n = 5
            op = self._rng.choice(["EX", "AX", "EF", "AG"])

        trans, labels = self._build_kripke(n)
        state = f"s{self._rng.randint(0, n - 1)}"
        prop = self._rng.choice(["p", "q"])

        if op == "EX":
            result = self._eval_ex(state, prop, trans, labels)
        elif op == "AX":
            result = self._eval_ax(state, prop, trans, labels)
        elif op == "EF":
            result = self._eval_ef(state, prop, trans, labels)
        else:
            result = self._eval_ag(state, prop, trans, labels)

        # Format transitions and labels compactly
        trans_str = "; ".join(
            f"{s}->{','.join(ts)}" for s, ts in sorted(trans.items())
        )
        label_str = "; ".join(
            f"{s}:{{{','.join(sorted(ls))}}}"
            for s, ls in sorted(labels.items())
        )

        successors = trans.get(state, [])
        succ_labels = [
            f"{s}:{{{','.join(sorted(labels.get(s, set())))}}}"
            for s in successors
        ]

        problem = (f"K: {trans_str}; L: {label_str}; "
                   f"check {op}({prop}) at {state}")

        steps = [
            f"state: {state}, successors: {successors}",
            f"successor labels: {succ_labels}",
            f"{op}({prop}) at {state} = {result}",
        ]

        return problem, {
            "op": op, "prop": prop, "state": state,
            "result": result, "steps_detail": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps_detail"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            True or False as a string.
        """
        return str(sd["result"])


# ===================================================================
# 5. LTL TO BUCHI AUTOMATON (tier 7)
# ===================================================================

@register
class LTLToBuchiGenerator(StepGenerator):
    """Convert simple LTL formula to Buchi automaton states.

    Template-based conversion for Gp (globally p), Fp (eventually p),
    and pUq (p until q).

    Difficulty scaling:
        Difficulty 1-3: Gp or Fp.
        Difficulty 4-6: pUq.
        Difficulty 7-8: negated formulas.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ltl_to_buchi"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["temporal_logic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "convert LTL formula to Buchi automaton"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an LTL-to-Buchi conversion problem.

        Args:
            difficulty: Controls formula complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        prop = self._rng.choice(["p", "q", "r"])
        prop2 = self._rng.choice([x for x in ["p", "q", "r"] if x != prop])

        if difficulty <= 3:
            formula_type = self._rng.choice(["Gp", "Fp"])
        elif difficulty <= 6:
            formula_type = "pUq"
        else:
            formula_type = self._rng.choice(["neg_Gp", "neg_Fp"])

        if formula_type == "Gp":
            formula = f"G({prop})"
            states = ["q0"]
            accepting = ["q0"]
            transitions = [f"q0 --{prop}--> q0"]
            explanation = (f"G({prop}) requires {prop} in every state; "
                          f"single accepting state with self-loop on {prop}")
        elif formula_type == "Fp":
            formula = f"F({prop})"
            states = ["q0", "q1"]
            accepting = ["q1"]
            transitions = [
                f"q0 --true--> q0",
                f"q0 --{prop}--> q1",
                f"q1 --true--> q1",
            ]
            explanation = (f"F({prop}) waits then sees {prop}; "
                          f"q0 waits, q1 accepts")
        elif formula_type == "pUq":
            formula = f"({prop})U({prop2})"
            states = ["q0", "q1"]
            accepting = ["q1"]
            transitions = [
                f"q0 --{prop}--> q0",
                f"q0 --{prop2}--> q1",
                f"q1 --true--> q1",
            ]
            explanation = (f"({prop})U({prop2}) holds {prop} until {prop2}; "
                          f"q0 loops on {prop}, transitions to q1 on {prop2}")
        elif formula_type == "neg_Gp":
            formula = f"!G({prop}) = F(!{prop})"
            states = ["q0", "q1"]
            accepting = ["q1"]
            transitions = [
                f"q0 --true--> q0",
                f"q0 --!{prop}--> q1",
                f"q1 --true--> q1",
            ]
            explanation = (f"!G({prop}) = F(!{prop}); "
                          f"accept when !{prop} is eventually seen")
        else:  # neg_Fp
            formula = f"!F({prop}) = G(!{prop})"
            states = ["q0"]
            accepting = ["q0"]
            transitions = [f"q0 --!{prop}--> q0"]
            explanation = (f"!F({prop}) = G(!{prop}); "
                          f"stay in accepting state only if !{prop}")

        problem = f"convert LTL formula {formula} to Buchi automaton"

        return problem, {
            "formula": formula,
            "states": states,
            "accepting": accepting,
            "transitions": transitions,
            "explanation": explanation,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"formula: {sd['formula']}",
            f"states: {sd['states']}",
            f"accepting: {sd['accepting']}",
        ]
        steps.extend([f"  {t}" for t in sd["transitions"]])
        steps.append(sd["explanation"])
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Automaton description string.
        """
        trans_str = ", ".join(sd["transitions"])
        return (f"states={sd['states']}, "
                f"accepting={sd['accepting']}, "
                f"transitions=[{trans_str}]")


# ===================================================================
# 6. BISIMULATION CHECK (tier 6)
# ===================================================================

@register
class BisimulationCheckGenerator(StepGenerator):
    """Check if two states in a labeled transition system are bisimilar.

    Two states are bisimilar if they have the same labels and for
    every transition from one, a matching transition exists from the other.

    Difficulty scaling:
        Difficulty 1-3: 3 states, 1 action.
        Difficulty 4-6: 4 states, 2 actions.
        Difficulty 7-8: 5 states, 2 actions.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bisimulation_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "check bisimulation between two states in LTS"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bisimulation checking problem.

        Args:
            difficulty: Controls LTS size and action count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 3
            actions = ["a"]
        elif difficulty <= 6:
            n = 4
            actions = ["a", "b"]
        else:
            n = 5
            actions = ["a", "b"]

        states = [f"s{i}" for i in range(n)]
        props = ["p", "q"]

        # Assign labels
        labels = {}
        for s in states:
            labels[s] = set()
            for pr in props:
                if self._rng.random() < 0.5:
                    labels[s].add(pr)

        # Build transitions
        transitions = {s: {} for s in states}
        for s in states:
            for act in actions:
                if self._rng.random() < 0.7:
                    target = self._rng.choice(states)
                    transitions[s][act] = target

        # Pick two states to compare
        s1, s2 = self._rng.sample(states, 2)

        # Check bisimulation (simplified: same labels + matching transitions)
        same_labels = labels[s1] == labels[s2]
        matching_trans = True
        mismatch_detail = ""
        if same_labels:
            for act in actions:
                t1 = transitions[s1].get(act)
                t2 = transitions[s2].get(act)
                if (t1 is None) != (t2 is None):
                    matching_trans = False
                    mismatch_detail = (f"action {act}: {s1} has "
                                      f"{'no ' if t1 is None else ''}"
                                      f"transition, {s2} has "
                                      f"{'no ' if t2 is None else ''}"
                                      f"transition")
                    break
                if t1 is not None and t2 is not None:
                    if labels.get(t1, set()) != labels.get(t2, set()):
                        matching_trans = False
                        mismatch_detail = (f"action {act}: targets {t1}, {t2}"
                                          f" have different labels")
                        break

        bisimilar = same_labels and matching_trans

        # Format LTS
        trans_parts = []
        for s in states:
            for act, tgt in sorted(transitions[s].items()):
                trans_parts.append(f"{s}--{act}-->{tgt}")
        label_parts = [f"{s}:{{{','.join(sorted(labels[s]))}}}"
                       for s in states]

        problem = (f"LTS: {'; '.join(trans_parts)}; "
                   f"labels: {'; '.join(label_parts)}; "
                   f"check {s1} ~ {s2}")

        steps = [
            f"labels({s1})={sorted(labels[s1])}, "
            f"labels({s2})={sorted(labels[s2])}",
            f"same labels: {same_labels}",
        ]
        if same_labels:
            steps.append(f"check transition matching")
            if not matching_trans:
                steps.append(f"mismatch: {mismatch_detail}")
            else:
                steps.append("all transitions match")
        steps.append(f"bisimilar: {bisimilar}")

        return problem, {
            "s1": s1, "s2": s2,
            "bisimilar": bisimilar,
            "steps_detail": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps_detail"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            BISIMILAR or NOT BISIMILAR.
        """
        return "BISIMILAR" if sd["bisimilar"] else "NOT BISIMILAR"


# ===================================================================
# 7. ABSTRACTION REFINEMENT (tier 7)
# ===================================================================

@register
class AbstractionRefinementGenerator(StepGenerator):
    """Simulate one CEGAR iteration: abstract, check, refine.

    Given a small concrete system, build an abstraction, check a property,
    and if a spurious counterexample is found, refine the abstraction.

    Difficulty scaling:
        Difficulty 1-4: 4 concrete states, 2 abstract states.
        Difficulty 5-8: 6 concrete states, 3 abstract states.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "abstraction_refinement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["ctl_model_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "perform one CEGAR iteration: abstract, check, refine"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CEGAR abstraction refinement problem.

        Args:
            difficulty: Controls system size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n_concrete = 4
            n_abstract = 2
        else:
            n_concrete = 6
            n_abstract = 3

        concrete = [f"c{i}" for i in range(n_concrete)]
        abstract = [f"a{i}" for i in range(n_abstract)]

        # Partition concrete into abstract
        mapping = {}
        for i, c in enumerate(concrete):
            mapping[c] = abstract[i % n_abstract]

        # Labels on concrete
        prop = self._rng.choice(["safe", "live"])
        concrete_labels = {}
        for c in concrete:
            concrete_labels[c] = self._rng.random() < 0.6

        # Abstract labels (overapproximate: True if any concrete member True)
        abstract_labels = {a: False for a in abstract}
        for c, a in mapping.items():
            if concrete_labels[c]:
                abstract_labels[a] = True

        # Check AG(prop) on abstract
        # Spurious if abstract says False but concrete is fine
        abstract_holds = all(abstract_labels.values())
        concrete_holds = all(concrete_labels.values())
        spurious = (not abstract_holds) and concrete_holds
        needs_refine = not abstract_holds

        mapping_str = ", ".join(f"{c}->{a}" for c, a in sorted(mapping.items()))
        concrete_str = ", ".join(
            f"{c}:{prop}" if v else f"{c}:!{prop}"
            for c, v in sorted(concrete_labels.items())
        )
        abstract_str = ", ".join(
            f"{a}:{prop}" if v else f"{a}:!{prop}"
            for a, v in sorted(abstract_labels.items())
        )

        problem = (f"concrete: {concrete_str}; "
                   f"mapping: {mapping_str}; "
                   f"check AG({prop})")

        steps = [
            f"abstract labels: {abstract_str}",
            f"AG({prop}) on abstract: {abstract_holds}",
        ]
        if needs_refine:
            if spurious:
                steps.append("counterexample is SPURIOUS in concrete")
                steps.append("refine: split abstract state to separate"
                            " violating concrete states")
            else:
                steps.append("counterexample is GENUINE")
                steps.append("property violated in concrete system")
        else:
            steps.append("property holds, no refinement needed")

        return problem, {
            "abstract_holds": abstract_holds,
            "concrete_holds": concrete_holds,
            "spurious": spurious,
            "needs_refine": needs_refine,
            "steps_detail": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps_detail"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Verification result and action.
        """
        if not sd["needs_refine"]:
            return "HOLDS"
        if sd["spurious"]:
            return "SPURIOUS, REFINE"
        return "VIOLATED"


# ===================================================================
# 8. INVARIANT SYNTHESIS (tier 7)
# ===================================================================

@register
class InvariantSynthesisGenerator(StepGenerator):
    """Synthesize a loop invariant from a template.

    Given pre/post-conditions and a loop body, find coefficients
    for a linear invariant template that satisfies initiation,
    consecution, and termination conditions.

    Difficulty scaling:
        Difficulty 1-4: single-variable invariant.
        Difficulty 5-8: two-variable invariant.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "invariant_synthesis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["loop_invariant_verify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "synthesize loop invariant from template"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an invariant synthesis problem.

        Args:
            difficulty: Controls invariant complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            # Pattern: {x=A} while x<N do x:=x+1 {x=N}
            a = self._rng.randint(0, 5)
            n = a + self._rng.randint(2, 6)
            pre = f"x={a}"
            guard = f"x<{n}"
            body = "x:=x+1"
            post = f"x={n}"
            template = "I: x>=A AND x<=N"
            invariant = f"x>={a} AND x<={n}"
            steps = [
                f"template: x>=? AND x<=?",
                f"initiation: x={a} => x>={a} AND x<={n}: True",
                f"consecution: x>={a} AND x<{n} AND x:=x+1"
                f" => x+1>={a} AND x+1<={n}: True (since x<{n})",
                f"termination: x>={a} AND x<={n} AND NOT(x<{n})"
                f" => x={n}: True",
                f"invariant: {invariant}",
            ]
        else:
            # Pattern: {x=0, s=0} while x<N do s:=s+x; x:=x+1 {s=N*(N-1)/2}
            n = self._rng.randint(3, 6 + difficulty)
            target = n * (n - 1) // 2
            pre = "x=0, s=0"
            guard = f"x<{n}"
            body = "s:=s+x; x:=x+1"
            post = f"s={target}"
            template = "I: s=x*(x-1)/2 AND x<=N"
            invariant = f"s=x*(x-1)/2 AND x<={n}"
            steps = [
                "template: s=x*(x-1)/2 AND x<=?",
                f"initiation: x=0,s=0 => s=0*(0-1)/2=0 AND 0<={n}: True",
                f"consecution: assume I AND x<{n}, after s:=s+x; x:=x+1",
                f"  s'=s+x=x*(x-1)/2+x=x*(x+1)/2",
                f"  x'=x+1, s'=x'*(x'-1)/2: True",
                f"termination: I AND x={n} => s={n}*({n}-1)/2={target}: True",
                f"invariant: {invariant}",
            ]

        problem = (f"pre: {pre}; while {guard} do {body}; post: {post}; "
                   f"template: {template}")

        return problem, {
            "invariant": invariant,
            "steps_detail": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps_detail"]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Synthesized invariant as a string.
        """
        return sd["invariant"]
