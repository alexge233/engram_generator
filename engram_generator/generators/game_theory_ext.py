"""Extended game theory generators.

6 generators across tiers 5-6.
"""
from itertools import permutations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class ExtensiveFormGenerator(StepGenerator):
    """Solve a 2-player extensive form game by backward induction.

    Generates a binary decision tree with 2-3 decision nodes and
    computes the subgame-perfect equilibrium via backward induction.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "extensive_form"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["minimax"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "solve extensive form game by backward induction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a binary game tree and solve via backward induction.

        Args:
            difficulty: Difficulty level controlling payoff range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        r = 3 + difficulty
        # 3-node tree: root (P1) -> left child (P2) -> two leaves,
        #                         -> right child (P2) -> two leaves
        leaves = [
            (self._rng.randint(-r, r), self._rng.randint(-r, r))
            for _ in range(4)
        ]
        # P2 at left node picks max of own payoff (index 1)
        if leaves[0][1] >= leaves[1][1]:
            p2_left_choice = "L"
            p2_left_payoff = leaves[0]
        else:
            p2_left_choice = "R"
            p2_left_payoff = leaves[1]
        # P2 at right node
        if leaves[2][1] >= leaves[3][1]:
            p2_right_choice = "L"
            p2_right_payoff = leaves[2]
        else:
            p2_right_choice = "R"
            p2_right_payoff = leaves[3]
        # P1 at root picks max of own payoff (index 0)
        if p2_left_payoff[0] >= p2_right_payoff[0]:
            p1_choice = "L"
            outcome = p2_left_payoff
        else:
            p1_choice = "R"
            outcome = p2_right_payoff
        leaves_str = " ".join(f"({a},{b})" for a, b in leaves)
        problem = (
            f"extensive form: P1 root, P2 at each child. "
            f"leaves L-R: {leaves_str}. backward induction?"
        )
        return problem, {
            "leaves": leaves,
            "p2_left": p2_left_choice,
            "p2_right": p2_right_choice,
            "p1": p1_choice,
            "outcome": outcome,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps from backward induction.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings in execution order.
        """
        lv = sd["leaves"]
        return [
            f"P2 left: {lv[0]} vs {lv[1]} -> {sd['p2_left']}",
            f"P2 right: {lv[2]} vs {lv[3]} -> {sd['p2_right']}",
            f"P1 root: compare P2 outcomes -> {sd['p1']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the subgame-perfect equilibrium outcome.

        Args:
            sd: Solution data dict.

        Returns:
            Outcome payoff pair.
        """
        return f"({sd['outcome'][0]},{sd['outcome'][1]})"


@register
class RepeatedGameGenerator(StepGenerator):
    """Compute threshold discount factor for cooperation in repeated PD.

    Uses the folk theorem condition delta >= (T-R)/(T-P) where T is
    temptation, R is reward, P is punishment, S is sucker payoff.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "repeated_game"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["nash_equilibrium"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute discount factor threshold for cooperation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a repeated prisoner's dilemma with TRPS payoffs.

        Args:
            difficulty: Difficulty level controlling payoff range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        # Ensure T > R > P > S
        base = self._rng.randint(1, 3 + difficulty)
        s_val = base
        p_val = s_val + self._rng.randint(1, 2 + difficulty)
        r_val = p_val + self._rng.randint(1, 2 + difficulty)
        t_val = r_val + self._rng.randint(1, 2 + difficulty)
        delta = round((t_val - r_val) / (t_val - p_val), 4)
        problem = (
            f"repeated PD: T={t_val}, R={r_val}, P={p_val}, S={s_val}. "
            f"min delta for cooperation?"
        )
        return problem, {
            "T": t_val, "R": r_val, "P": p_val, "S": s_val,
            "delta": delta,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show the folk theorem computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"T-R = {sd['T']}-{sd['R']} = {sd['T'] - sd['R']}",
            f"T-P = {sd['T']}-{sd['P']} = {sd['T'] - sd['P']}",
            f"delta >= (T-R)/(T-P) = {sd['delta']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the threshold discount factor.

        Args:
            sd: Solution data dict.

        Returns:
            Threshold delta value.
        """
        return f"delta >= {sd['delta']}"


@register
class BayesianGameGenerator(StepGenerator):
    """Compute Bayesian Nash Equilibrium for a type-dependent game.

    Each player has a type (high/low) drawn with known probability.
    Computes expected payoffs and finds type-dependent best responses.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bayesian_game"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["nash_equilibrium"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find Bayesian Nash equilibrium"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2-player 2-type Bayesian game.

        Args:
            difficulty: Difficulty level controlling payoff range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        r = 3 + difficulty
        p_high = round(self._rng.uniform(0.2, 0.8), 2)
        p_low = round(1.0 - p_high, 2)
        # Payoffs for player 1: action A or B, given own type and opponent action
        # Simplified: P1 high type payoffs for (A,B) and P1 low type payoffs
        payoffs_high = {
            "A": self._rng.randint(1, r),
            "B": self._rng.randint(1, r),
        }
        payoffs_low = {
            "A": self._rng.randint(1, r),
            "B": self._rng.randint(1, r),
        }
        best_high = "A" if payoffs_high["A"] >= payoffs_high["B"] else "B"
        best_low = "A" if payoffs_low["A"] >= payoffs_low["B"] else "B"
        # Expected payoff for opponent facing this strategy
        exp_a = round(p_high * payoffs_high[best_high] + p_low * payoffs_low[best_low], 4)
        problem = (
            f"P(high)={p_high}, P(low)={p_low}. "
            f"high: A={payoffs_high['A']}, B={payoffs_high['B']}; "
            f"low: A={payoffs_low['A']}, B={payoffs_low['B']}. BNE?"
        )
        return problem, {
            "p_high": p_high, "p_low": p_low,
            "payoffs_high": payoffs_high, "payoffs_low": payoffs_low,
            "best_high": best_high, "best_low": best_low,
            "exp_payoff": exp_a,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show type-dependent best response computation.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        ph = sd["payoffs_high"]
        pl = sd["payoffs_low"]
        return [
            f"high type: A={ph['A']} vs B={ph['B']} -> {sd['best_high']}",
            f"low type: A={pl['A']} vs B={pl['B']} -> {sd['best_low']}",
            f"expected payoff = {sd['exp_payoff']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the BNE strategy profile.

        Args:
            sd: Solution data dict.

        Returns:
            Type-dependent strategy.
        """
        return f"high->{sd['best_high']}, low->{sd['best_low']}"


@register
class CorrelatedEquilibriumGenerator(StepGenerator):
    """Check correlated equilibrium conditions for a correlation device.

    Given a joint distribution over action pairs, verifies that no
    player has an incentive to deviate from the recommended action.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "correlated_equilibrium"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check correlated equilibrium conditions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2x2 game with a correlation device.

        Args:
            difficulty: Difficulty level controlling payoff range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        r = 3 + difficulty
        # 2x2 payoff matrix
        payoffs = [
            [(self._rng.randint(0, r), self._rng.randint(0, r)) for _ in range(2)]
            for _ in range(2)
        ]
        # Joint distribution (probabilities summing to 1)
        raw = [self._rng.randint(1, 10) for _ in range(4)]
        total = sum(raw)
        probs = [[round(raw[0] / total, 4), round(raw[1] / total, 4)],
                 [round(raw[2] / total, 4), round(raw[3] / total, 4)]]
        # Adjust last to ensure sum = 1
        probs[1][1] = round(1.0 - probs[0][0] - probs[0][1] - probs[1][0], 4)

        # Check CE conditions for row player
        # If told to play action i, should not prefer switching to j
        violations = []
        for i in range(2):
            row_prob = probs[i][0] + probs[i][1]
            if row_prob < 1e-9:
                continue
            j = 1 - i
            gain_stay = sum(probs[i][c] * payoffs[i][c][0] for c in range(2))
            gain_dev = sum(probs[i][c] * payoffs[j][c][0] for c in range(2))
            if gain_dev > gain_stay + 1e-9:
                violations.append(f"row {i}->{j}")

        # Check CE conditions for column player
        for c_act in range(2):
            col_prob = probs[0][c_act] + probs[1][c_act]
            if col_prob < 1e-9:
                continue
            c_alt = 1 - c_act
            gain_stay = sum(probs[r][c_act] * payoffs[r][c_act][1] for r in range(2))
            gain_dev = sum(probs[r][c_act] * payoffs[r][c_alt][1] for r in range(2))
            if gain_dev > gain_stay + 1e-9:
                violations.append(f"col {c_act}->{c_alt}")

        is_ce = len(violations) == 0
        mat_str = (
            f"[({payoffs[0][0][0]},{payoffs[0][0][1]}),"
            f"({payoffs[0][1][0]},{payoffs[0][1][1]})];"
            f"[({payoffs[1][0][0]},{payoffs[1][0][1]}),"
            f"({payoffs[1][1][0]},{payoffs[1][1][1]})]"
        )
        prob_str = (
            f"[{probs[0][0]},{probs[0][1]}];"
            f"[{probs[1][0]},{probs[1][1]}]"
        )
        problem = f"game: {mat_str}. device: {prob_str}. CE?"
        return problem, {
            "payoffs": payoffs, "probs": probs,
            "is_ce": is_ce, "violations": violations,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show deviation incentive checks.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        steps = ["check row player deviation incentives",
                 "check col player deviation incentives"]
        if sd["violations"]:
            steps.append(f"violations: {', '.join(sd['violations'])}")
        else:
            steps.append("no deviations profitable")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return whether the device is a correlated equilibrium.

        Args:
            sd: Solution data dict.

        Returns:
            YES or NO with violations.
        """
        if sd["is_ce"]:
            return "YES, correlated equilibrium"
        return f"NO, violations: {', '.join(sd['violations'])}"


@register
class ShapleyValueGenerator(StepGenerator):
    """Compute Shapley value for a 3-player cooperative game.

    Averages each player's marginal contribution over all permutations
    of the player set.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "shapley_value"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Shapley value for 3-player game"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 3-player coalitional game and compute Shapley values.

        Args:
            difficulty: Difficulty level controlling value range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        r = 5 * difficulty
        players = [0, 1, 2]
        # Characteristic function v(S) for all subsets
        v = {}
        v[frozenset()] = 0
        for p in players:
            v[frozenset([p])] = self._rng.randint(0, r)
        for i in range(3):
            for j in range(i + 1, 3):
                pair_val = v[frozenset([i])] + v[frozenset([j])]
                v[frozenset([i, j])] = pair_val + self._rng.randint(0, r // 2 + 1)
        grand_val = max(v[frozenset([0, 1])], v[frozenset([0, 2])], v[frozenset([1, 2])])
        v[frozenset(players)] = grand_val + self._rng.randint(0, r // 2 + 1)

        # Compute Shapley values
        phi = [0.0, 0.0, 0.0]
        perms = list(permutations(players))
        for perm in perms:
            coalition = set()
            for p in perm:
                marginal = v[frozenset(coalition | {p})] - v[frozenset(coalition)]
                phi[p] += marginal
                coalition.add(p)
        phi = [round(x / len(perms), 4) for x in phi]

        v_str = "; ".join(
            f"v({set(k)})={val}" for k, val in sorted(v.items(), key=lambda x: len(x[0]))
            if len(k) > 0
        )
        problem = f"3-player game: {v_str}. Shapley values?"
        return problem, {"v": {str(set(k)): val for k, val in v.items()}, "phi": phi}

    def _create_steps(self, sd: dict) -> list[str]:
        """Show Shapley value computation summary.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            "average marginal contributions over 6 permutations",
            f"phi_0 = {sd['phi'][0]}, phi_1 = {sd['phi'][1]}, phi_2 = {sd['phi'][2]}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the Shapley values.

        Args:
            sd: Solution data dict.

        Returns:
            Shapley value vector.
        """
        return f"phi = ({sd['phi'][0]}, {sd['phi'][1]}, {sd['phi'][2]})"


@register
class EvolutionaryStableGenerator(StepGenerator):
    """Check if a strategy is an Evolutionarily Stable Strategy (ESS).

    Verifies two conditions: E(s*,s*) > E(s,s*) or
    [E(s*,s*) = E(s,s*) and E(s*,s) > E(s,s)].
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "evolutionary_stable"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["nash_equilibrium"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check if strategy is ESS"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a symmetric 2x2 game and check ESS condition.

        Args:
            difficulty: Difficulty level controlling payoff range.

        Returns:
            Tuple of (problem text, solution data dict).
        """
        r = 3 + difficulty
        # Symmetric payoff matrix: a = E(s*,s*), b = E(s*,s), c = E(s,s*), d = E(s,s)
        a = self._rng.randint(0, r)  # E(s*, s*)
        b = self._rng.randint(0, r)  # E(s*, s)
        c = self._rng.randint(0, r)  # E(s, s*)
        d = self._rng.randint(0, r)  # E(s, s)

        if a > c:
            is_ess = True
            reason = "E(s*,s*) > E(s,s*)"
        elif a == c and b > d:
            is_ess = True
            reason = "E(s*,s*) = E(s,s*) and E(s*,s) > E(s,s)"
        else:
            is_ess = False
            if a < c:
                reason = "E(s*,s*) < E(s,s*)"
            else:
                reason = "E(s*,s*) = E(s,s*) but E(s*,s) <= E(s,s)"

        problem = (
            f"symmetric game: E(s*,s*)={a}, E(s*,s)={b}, "
            f"E(s,s*)={c}, E(s,s)={d}. is s* ESS?"
        )
        return problem, {
            "a": a, "b": b, "c": c, "d": d,
            "is_ess": is_ess, "reason": reason,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Show ESS condition checks.

        Args:
            sd: Solution data dict.

        Returns:
            Step strings.
        """
        return [
            f"check E(s*,s*)={sd['a']} vs E(s,s*)={sd['c']}",
            f"check E(s*,s)={sd['b']} vs E(s,s)={sd['d']}",
            sd["reason"],
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return whether the strategy is ESS.

        Args:
            sd: Solution data dict.

        Returns:
            YES or NO with reason.
        """
        return f"{'YES' if sd['is_ess'] else 'NO'}: {sd['reason']}"
