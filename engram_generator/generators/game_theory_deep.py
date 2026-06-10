"""Deep game theory generators.

8 generators across tiers 3-5 covering mixed strategy Nash equilibrium,
zero-sum game solutions, prisoner's dilemma analysis, chicken game,
battle of the sexes, Pareto efficiency, backward induction, and
first-price auction optimal bidding.
"""

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _fmt(value: float, decimals: int = 4) -> str:
    """Format a numeric value, stripping unnecessary trailing zeros.

    Args:
        value: Number to format.
        decimals: Maximum decimal places.

    Returns:
        Clean string representation.
    """
    rounded = round(value, decimals)
    if isinstance(rounded, float) and rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


# ---------------------------------------------------------------------------
# 1. Mixed Strategy Nash Equilibrium (tier 5)
# ---------------------------------------------------------------------------

@register
class MixedStrategyNEGenerator(StepGenerator):
    """Find the mixed strategy Nash equilibrium of a 2x2 game.

    Uses the indifference condition: player mixes so opponent is
    indifferent. p*u(T,L)+(1-p)*u(B,L) = p*u(T,R)+(1-p)*u(B,R).

    Difficulty scaling:
        d1-3: small positive payoffs.
        d4-6: mixed positive/negative payoffs.
        d7-8: larger payoff ranges.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mixed_strategy_ne"

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
        return "find mixed strategy Nash equilibrium"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2x2 game and compute mixed strategy NE.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 3 + difficulty
        low = -r // 2 if difficulty > 3 else 0
        # Generate payoffs ensuring no pure strategy NE dominates
        # Row player payoffs
        for _ in range(20):
            rp = [[self._rng.randint(low, r) for _ in range(2)] for _ in range(2)]
            cp = [[self._rng.randint(low, r) for _ in range(2)] for _ in range(2)]
            # Column player indifference for row player's mix
            # p such that col is indifferent: p*cp[0][0]+(1-p)*cp[1][0] = p*cp[0][1]+(1-p)*cp[1][1]
            denom_q = (rp[0][0] - rp[1][0]) - (rp[0][1] - rp[1][1])
            denom_p = (cp[0][0] - cp[0][1]) - (cp[1][0] - cp[1][1])
            if abs(denom_q) > 0 and abs(denom_p) > 0:
                q = (rp[1][1] - rp[1][0]) / denom_q
                p = (cp[1][1] - cp[1][0]) / denom_p
                if 0 < p < 1 and 0 < q < 1:
                    break
        else:
            # Fallback: matching pennies
            rp = [[1, -1], [-1, 1]]
            cp = [[-1, 1], [1, -1]]
            p, q = 0.5, 0.5
        p = round(p, 4)
        q = round(q, 4)
        # Expected payoff for row player
        eu_row = round(p * q * rp[0][0] + p * (1 - q) * rp[0][1]
                       + (1 - p) * q * rp[1][0] + (1 - p) * (1 - q) * rp[1][1], 4)
        mat_str = (
            f"row:[({rp[0][0]},{cp[0][0]}),({rp[0][1]},{cp[0][1]})];"
            f"[({rp[1][0]},{cp[1][0]}),({rp[1][1]},{cp[1][1]})]"
        )
        return (
            f"mixed NE: {mat_str}",
            {
                "rp": rp, "cp": cp,
                "p": p, "q": q,
                "eu_row": eu_row,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate mixed NE computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing indifference conditions and probabilities.
        """
        rp, cp = sd["rp"], sd["cp"]
        return [
            f"col indiff: p*{cp[0][0]}+(1-p)*{cp[1][0]} = p*{cp[0][1]}+(1-p)*{cp[1][1]}",
            f"p = {_fmt(sd['p'])} (row plays T)",
            f"row indiff: q*{rp[0][0]}+(1-q)*{rp[0][1]} = q*{rp[1][0]}+(1-q)*{rp[1][1]}",
            f"q = {_fmt(sd['q'])} (col plays L)",
            f"EU_row = {_fmt(sd['eu_row'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the mixed strategy NE.

        Args:
            sd: Solution data dict.

        Returns:
            Mixing probabilities.
        """
        return f"p={_fmt(sd['p'])}, q={_fmt(sd['q'])}"


# ---------------------------------------------------------------------------
# 2. Zero-Sum Game (tier 4)
# ---------------------------------------------------------------------------

@register
class ZeroSumGameGenerator(StepGenerator):
    """Solve a 2x2 zero-sum game by the maximin method.

    If no saddle point exists, compute the value of the game using
    V = (a*d - b*c) / (a + d - b - c) where the payoff matrix is
    [[a,b],[c,d]].

    Difficulty scaling:
        d1-3: small integers, saddle point exists.
        d4-6: no saddle point, compute mixed value.
        d7-8: larger payoffs, no saddle point.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "zero_sum_game"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "solve 2x2 zero-sum game"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2x2 zero-sum game and solve it.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 3 + difficulty
        if difficulty <= 3:
            # Create game with saddle point
            a = self._rng.randint(1, r)
            b = self._rng.randint(1, r)
            c = self._rng.randint(1, r)
            d = self._rng.randint(1, r)
        else:
            # Create game without saddle point
            for _ in range(20):
                a = self._rng.randint(-r, r)
                b = self._rng.randint(-r, r)
                c = self._rng.randint(-r, r)
                d = self._rng.randint(-r, r)
                denom = a + d - b - c
                if abs(denom) > 0:
                    # Check no saddle point
                    row_mins = [min(a, b), min(c, d)]
                    col_maxs = [max(a, c), max(b, d)]
                    maximin = max(row_mins)
                    minimax = min(col_maxs)
                    if maximin != minimax:
                        break
            else:
                a, b, c, d = 3, 1, 5, 2
                denom = a + d - b - c

        row_mins = [min(a, b), min(c, d)]
        col_maxs = [max(a, c), max(b, d)]
        maximin = max(row_mins)
        minimax = min(col_maxs)
        has_saddle = maximin == minimax
        if has_saddle:
            value = maximin
            p_opt = None
        else:
            denom = a + d - b - c
            value = round((a * d - b * c) / denom, 4) if denom != 0 else 0
            p_opt = round((d - c) / denom, 4) if denom != 0 else 0.5
        return (
            f"zero-sum: [[{a},{b}],[{c},{d}]]",
            {
                "a": a, "b": b, "c": c, "d": d,
                "maximin": maximin, "minimax": minimax,
                "has_saddle": has_saddle,
                "value": value, "p_opt": p_opt,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate zero-sum solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing maximin/minimax and value computation.
        """
        steps = [
            f"row mins: [min({sd['a']},{sd['b']}), min({sd['c']},{sd['d']})] = [{min(sd['a'],sd['b'])},{min(sd['c'],sd['d'])}]",
            f"maximin = {sd['maximin']}, minimax = {sd['minimax']}",
        ]
        if sd["has_saddle"]:
            steps.append(f"saddle point exists: V = {sd['value']}")
        else:
            denom = sd["a"] + sd["d"] - sd["b"] - sd["c"]
            steps.append(f"no saddle: V = ({sd['a']}*{sd['d']}-{sd['b']}*{sd['c']})/({denom})")
            steps.append(f"V = {_fmt(sd['value'])}, p* = {_fmt(sd['p_opt'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the game value.

        Args:
            sd: Solution data dict.

        Returns:
            Value of the game.
        """
        if sd["has_saddle"]:
            return f"V = {sd['value']} (saddle point)"
        return f"V = {_fmt(sd['value'])}, p* = {_fmt(sd['p_opt'])}"


# ---------------------------------------------------------------------------
# 3. Prisoner's Dilemma (tier 3)
# ---------------------------------------------------------------------------

@register
class PrisonersDilemmaGenerator(StepGenerator):
    """Analyse a prisoner's dilemma payoff matrix.

    Identifies the dominant strategy (Defect) and compares the Nash
    equilibrium payoff with the cooperative (mutual Cooperate) payoff.

    Difficulty scaling:
        d1-3: standard PD payoffs, small numbers.
        d4-6: PD with varied payoffs.
        d7-8: larger payoff ranges.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "prisoners_dilemma"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dominant_strategy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "analyse prisoner's dilemma"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PD payoff matrix satisfying T>R>P>S.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        base = self._rng.randint(0, difficulty)
        s_val = base
        p_val = s_val + self._rng.randint(1, 2 + difficulty)
        r_val = p_val + self._rng.randint(1, 2 + difficulty)
        t_val = r_val + self._rng.randint(1, 2 + difficulty)
        # Payoff matrix: (C,C)=(R,R), (C,D)=(S,T), (D,C)=(T,S), (D,D)=(P,P)
        nash_payoff = (p_val, p_val)
        coop_payoff = (r_val, r_val)
        loss = coop_payoff[0] - nash_payoff[0]
        return (
            f"PD: T={t_val}, R={r_val}, P={p_val}, S={s_val}",
            {
                "T": t_val, "R": r_val, "P": p_val, "S": s_val,
                "nash": nash_payoff, "coop": coop_payoff,
                "loss": loss,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate PD analysis steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing dominant strategy and payoff comparison.
        """
        return [
            f"T={sd['T']} > R={sd['R']} > P={sd['P']} > S={sd['S']}",
            "dominant strategy: Defect (D strictly dominates C for both)",
            f"Nash (D,D) = ({sd['P']},{sd['P']})",
            f"cooperative (C,C) = ({sd['R']},{sd['R']})",
            f"cooperation gain per player = {sd['loss']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the PD analysis result.

        Args:
            sd: Solution data dict.

        Returns:
            Dominant strategy and Nash vs cooperative payoffs.
        """
        return f"dominant=D, Nash=({sd['P']},{sd['P']}), coop=({sd['R']},{sd['R']})"


# ---------------------------------------------------------------------------
# 4. Chicken Game (tier 4)
# ---------------------------------------------------------------------------

@register
class ChickenGameGenerator(StepGenerator):
    """Find all Nash equilibria in a chicken (hawk-dove) game.

    The game has 2 pure strategy NE and 1 mixed strategy NE.
    Payoffs satisfy T > S > P > W (or similar chicken structure).

    Difficulty scaling:
        d1-3: small payoffs, symmetric.
        d4-6: medium payoffs.
        d7-8: larger payoffs.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chicken_game"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "find Nash equilibria in chicken game"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a chicken game and find all NE.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Chicken: (Swerve, Swerve)=(0,0), (Swerve, Straight)=(-1,W),
        #          (Straight, Swerve)=(W,-1), (Straight, Straight)=(-D,-D)
        w = self._rng.randint(1, 2 + difficulty)
        d_val = self._rng.randint(w + 1, w + 3 + difficulty)
        # Payoff matrix (row=P1, col=P2): Swerve=0, Straight=1
        # (S,S)=(0,0), (S,St)=(-1,w), (St,S)=(w,-1), (St,St)=(-d,-d)
        matrix = [
            [(0, 0), (-1, w)],
            [(w, -1), (-d_val, -d_val)],
        ]
        # Pure NE: (Swerve,Straight) and (Straight,Swerve)
        pure_ne = [(0, 1), (1, 0)]
        # Mixed NE: p = prob(Swerve)
        # Indifference for P2: p*0 + (1-p)*(-1) = p*w + (1-p)*(-d)
        # -1+p = pw - d + dp => -1+p = pw + dp - d
        # -1 + p - pw - dp + d = 0 => p(1 - w - d) = 1 - d
        denom = 1 - w - (-d_val)
        # Correct: p*(0) + (1-p)*w = p*(-1) + (1-p)*(-d_val)
        # Column player indiff between swerve and straight
        # if col swerves: payoff = p*0 + (1-p)*(-1) = -(1-p)
        # if col goes straight: payoff = p*w + (1-p)*(-d_val)
        # -(1-p) = p*w + (1-p)*(-d_val)
        # -1+p = pw - d_val + p*d_val
        # -1 + p - pw - p*d_val + d_val = 0
        # p(1 - w - d_val) = 1 - d_val
        denom_mix = 1 - w - d_val
        if abs(denom_mix) > 0:
            p_mix = round((1 - d_val) / denom_mix, 4)
        else:
            p_mix = 0.5
        mat_str = (
            f"[(0,0),(-1,{w})];[({w},-1),({-d_val},{-d_val})]"
        )
        return (
            f"chicken: {mat_str}",
            {
                "w": w, "d": d_val,
                "pure_ne": pure_ne,
                "p_mix": p_mix,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate chicken game NE computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing pure and mixed NE.
        """
        return [
            "pure NE 1: (Swerve, Straight) = (-1, w)",
            "pure NE 2: (Straight, Swerve) = (w, -1)",
            f"mixed: p(Swerve) = {_fmt(sd['p_mix'])}",
            f"3 Nash equilibria total",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return all Nash equilibria.

        Args:
            sd: Solution data dict.

        Returns:
            Pure and mixed NE.
        """
        return f"pure: (S,St),(St,S); mixed: p={_fmt(sd['p_mix'])}"


# ---------------------------------------------------------------------------
# 5. Battle of the Sexes (tier 4)
# ---------------------------------------------------------------------------

@register
class BattleOfSexesGenerator(StepGenerator):
    """Find Nash equilibria in a battle of the sexes game.

    Two players prefer to coordinate but disagree on which outcome.
    Has 2 pure NE and 1 mixed NE.

    Difficulty scaling:
        d1-3: small payoffs (e.g. 3,2 vs 2,3).
        d4-6: medium payoffs.
        d7-8: larger payoffs with asymmetry.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "battle_of_sexes"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "find Nash equilibria in battle of the sexes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BoS game and find all NE.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # P1 prefers A, P2 prefers B
        a_val = self._rng.randint(2, 3 + difficulty)
        b_val = self._rng.randint(1, a_val - 1) if a_val > 1 else 1
        # Matrix: (A,A)=(a,b), (A,B)=(0,0), (B,A)=(0,0), (B,B)=(b,a)
        matrix = [
            [(a_val, b_val), (0, 0)],
            [(0, 0), (b_val, a_val)],
        ]
        # Pure NE: (A,A) and (B,B)
        # Mixed NE: p*a + (1-p)*0 = p*0 + (1-p)*b => pa = (1-p)b => p = b/(a+b)
        # For P2: q*b + (1-q)*0 = q*0 + (1-q)*a => qb = (1-q)a => q = a/(a+b)
        p_mix = round(b_val / (a_val + b_val), 4)
        q_mix = round(a_val / (a_val + b_val), 4)
        mat_str = (
            f"[({a_val},{b_val}),(0,0)];[(0,0),({b_val},{a_val})]"
        )
        return (
            f"BoS: {mat_str}",
            {
                "a": a_val, "b": b_val,
                "p_mix": p_mix, "q_mix": q_mix,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate BoS NE computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing pure and mixed NE.
        """
        return [
            f"pure NE 1: (A,A) -> ({sd['a']},{sd['b']})",
            f"pure NE 2: (B,B) -> ({sd['b']},{sd['a']})",
            f"P1 indifference: p*{sd['a']} = (1-p)*{sd['b']} -> p = {_fmt(sd['p_mix'])}",
            f"P2 indifference: q*{sd['b']} = (1-q)*{sd['a']} -> q = {_fmt(sd['q_mix'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return all Nash equilibria.

        Args:
            sd: Solution data dict.

        Returns:
            Pure and mixed NE.
        """
        return f"pure: (A,A),(B,B); mixed: p={_fmt(sd['p_mix'])}, q={_fmt(sd['q_mix'])}"


# ---------------------------------------------------------------------------
# 6. Pareto Efficiency (tier 4)
# ---------------------------------------------------------------------------

@register
class ParetoEfficiencyGenerator(StepGenerator):
    """Identify Pareto-efficient outcomes in a 2x2 game.

    An outcome is Pareto-efficient if no player can improve without
    hurting another. Checks all four outcomes for Pareto dominance.

    Difficulty scaling:
        d1-3: clear Pareto ranking, small payoffs.
        d4-6: multiple Pareto-efficient outcomes.
        d7-8: larger payoffs, subtle dominance relations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pareto_efficiency"

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
            Short task description.
        """
        return "identify Pareto-efficient outcomes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2x2 game and find Pareto-efficient outcomes.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 3 + difficulty
        outcomes = []
        for row in range(2):
            for col in range(2):
                outcomes.append(
                    (row, col,
                     self._rng.randint(0, r),
                     self._rng.randint(0, r))
                )
        # Check Pareto efficiency: outcome i is Pareto-dominated if
        # there exists j where both players are >= and at least one is >
        pareto = []
        for i in range(4):
            dominated = False
            for j in range(4):
                if i == j:
                    continue
                if (outcomes[j][2] >= outcomes[i][2] and
                        outcomes[j][3] >= outcomes[i][3] and
                        (outcomes[j][2] > outcomes[i][2] or
                         outcomes[j][3] > outcomes[i][3])):
                    dominated = True
                    break
            if not dominated:
                pareto.append((outcomes[i][0], outcomes[i][1]))
        mat_str = (
            f"[({outcomes[0][2]},{outcomes[0][3]}),({outcomes[1][2]},{outcomes[1][3]})];"
            f"[({outcomes[2][2]},{outcomes[2][3]}),({outcomes[3][2]},{outcomes[3][3]})]"
        )
        return (
            f"Pareto: {mat_str}",
            {"outcomes": outcomes, "pareto": pareto},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Pareto efficiency analysis steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing dominance checks.
        """
        steps = []
        for i, o in enumerate(sd["outcomes"]):
            pos = f"({o[0]},{o[1]})"
            is_pareto = (o[0], o[1]) in sd["pareto"]
            steps.append(f"{pos}: ({o[2]},{o[3]}) -> {'Pareto-efficient' if is_pareto else 'dominated'}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Pareto-efficient outcomes.

        Args:
            sd: Solution data dict.

        Returns:
            List of Pareto-efficient outcome positions.
        """
        pe_str = ", ".join(f"({r},{c})" for r, c in sd["pareto"])
        return f"Pareto-efficient: {pe_str}"


# ---------------------------------------------------------------------------
# 7. Backward Induction (tier 5)
# ---------------------------------------------------------------------------

@register
class BackwardInductionGenerator(StepGenerator):
    """Solve an extensive form game by backward induction.

    Generates a sequential game with 3-4 decision nodes and
    computes the subgame perfect equilibrium by working backward
    from terminal nodes.

    Difficulty scaling:
        d1-3: 3-node tree, small payoffs.
        d4-6: 4-node tree, medium payoffs.
        d7-8: 4-node tree, larger payoffs with negative values.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "backward_induction"

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
        return "solve game by backward induction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sequential game tree and solve by backward induction.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        r = 3 + difficulty
        low = -r // 2 if difficulty > 3 else 0
        if difficulty <= 3:
            # 3-node tree: root P1 -> (L: leaf, R: P2 node -> (L: leaf, R: leaf))
            leaves = [
                (self._rng.randint(low, r), self._rng.randint(low, r))
                for _ in range(3)
            ]
            # P2 at right subtree: picks max of own payoff (index 1)
            if leaves[1][1] >= leaves[2][1]:
                p2_choice = "L"
                p2_payoff = leaves[1]
            else:
                p2_choice = "R"
                p2_payoff = leaves[2]
            # P1 at root: compare leaf[0] with P2's outcome
            if leaves[0][0] >= p2_payoff[0]:
                p1_choice = "L"
                outcome = leaves[0]
            else:
                p1_choice = "R"
                outcome = p2_payoff
            n_nodes = 3
            leaves_str = " ".join(f"({a},{b})" for a, b in leaves)
            problem = f"3-node tree. P1 root: L->({leaves[0][0]},{leaves[0][1]}), R->P2. P2: L,R. Leaves: {leaves_str}"
            sd = {
                "n_nodes": n_nodes, "leaves": leaves,
                "p2_choice": p2_choice, "p2_payoff": p2_payoff,
                "p1_choice": p1_choice, "outcome": outcome,
            }
        else:
            # 4-node tree: root P1 -> L: P2 node, R: P2 node
            leaves = [
                (self._rng.randint(low, r), self._rng.randint(low, r))
                for _ in range(4)
            ]
            # P2 left
            if leaves[0][1] >= leaves[1][1]:
                p2_l_choice = "L"
                p2_l_payoff = leaves[0]
            else:
                p2_l_choice = "R"
                p2_l_payoff = leaves[1]
            # P2 right
            if leaves[2][1] >= leaves[3][1]:
                p2_r_choice = "L"
                p2_r_payoff = leaves[2]
            else:
                p2_r_choice = "R"
                p2_r_payoff = leaves[3]
            # P1
            if p2_l_payoff[0] >= p2_r_payoff[0]:
                p1_choice = "L"
                outcome = p2_l_payoff
            else:
                p1_choice = "R"
                outcome = p2_r_payoff
            n_nodes = 4
            leaves_str = " ".join(f"({a},{b})" for a, b in leaves)
            problem = f"4-node tree. P1->P2(L),P2(R). Leaves L-R: {leaves_str}"
            sd = {
                "n_nodes": n_nodes, "leaves": leaves,
                "p2_l_choice": p2_l_choice, "p2_l_payoff": p2_l_payoff,
                "p2_r_choice": p2_r_choice, "p2_r_payoff": p2_r_payoff,
                "p1_choice": p1_choice, "outcome": outcome,
            }
        return problem, sd

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate backward induction solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing subgame solutions and root decision.
        """
        steps = []
        if sd["n_nodes"] == 3:
            lv = sd["leaves"]
            steps.append(f"P2: {lv[1]} vs {lv[2]} -> {sd['p2_choice']} = {sd['p2_payoff']}")
            steps.append(f"P1: {lv[0]} vs {sd['p2_payoff']} -> {sd['p1_choice']}")
        else:
            lv = sd["leaves"]
            steps.append(f"P2 left: {lv[0]} vs {lv[1]} -> {sd['p2_l_choice']} = {sd['p2_l_payoff']}")
            steps.append(f"P2 right: {lv[2]} vs {lv[3]} -> {sd['p2_r_choice']} = {sd['p2_r_payoff']}")
            steps.append(f"P1: {sd['p2_l_payoff']} vs {sd['p2_r_payoff']} -> {sd['p1_choice']}")
        steps.append(f"SPE outcome: {sd['outcome']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the subgame perfect equilibrium outcome.

        Args:
            sd: Solution data dict.

        Returns:
            SPE outcome payoff pair.
        """
        o = sd["outcome"]
        return f"SPE: ({o[0]},{o[1]})"


# ---------------------------------------------------------------------------
# 8. First-Price Auction (tier 5)
# ---------------------------------------------------------------------------

@register
class AuctionFirstPriceGenerator(StepGenerator):
    """Compute optimal bidding in a first-price sealed-bid auction.

    With n bidders and value v drawn from Uniform[0, V], the
    symmetric equilibrium bid is b = v * (n-1) / n.  Expected
    revenue is (n-1)/(n+1) * V.

    Difficulty scaling:
        d1-3: n=2, integer values.
        d4-6: n=3-4, medium values.
        d7-8: n=5-8, larger values.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "auction_first_price"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "compute optimal first-price auction bid"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate auction parameters and compute optimal bid.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 2
            v_max = self._rng.randint(10, 50)
        elif difficulty <= 6:
            n = self._rng.randint(3, 4)
            v_max = self._rng.randint(20, 100)
        else:
            n = self._rng.randint(5, 8)
            v_max = self._rng.randint(50, 200)
        value = self._rng.randint(1, v_max)
        bid = round(value * (n - 1) / n, 4)
        exp_revenue = round(v_max * (n - 1) / (n + 1), 4)
        return (
            f"first-price auction: n={n}, v={value}, V_max={v_max}",
            {
                "n": n, "value": value, "v_max": v_max,
                "bid": bid, "exp_revenue": exp_revenue,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate auction computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing equilibrium bid and expected revenue.
        """
        n = sd["n"]
        return [
            f"n = {n} bidders, value = {sd['value']}",
            f"optimal bid b = v*(n-1)/n = {sd['value']}*{n-1}/{n}",
            f"b = {_fmt(sd['bid'])}",
            f"E[revenue] = V*(n-1)/(n+1) = {sd['v_max']}*{n-1}/{n+1} = {_fmt(sd['exp_revenue'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the optimal bid and expected revenue.

        Args:
            sd: Solution data dict.

        Returns:
            Bid and expected revenue.
        """
        return f"bid = {_fmt(sd['bid'])}, E[revenue] = {_fmt(sd['exp_revenue'])}"
