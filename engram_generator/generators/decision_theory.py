"""Decision theory generators.

8 generators across tiers 5-7 covering expected utility, risk dominance,
Bayesian updating, value of information, multi-criteria decision making,
prospect theory, sequential decisions, and mechanism design.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _z_inv_approx(p: float) -> float:
    """Approximate inverse normal CDF (probit) using Abramowitz & Stegun.

    Args:
        p: Probability in (0, 1).

    Returns:
        Approximate z-score.
    """
    if p <= 0.0 or p >= 1.0:
        return 0.0
    sign = 1.0
    if p < 0.5:
        p = 1.0 - p
        sign = -1.0
    t = math.sqrt(-2.0 * math.log(1.0 - p))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    z = t - (c0 + c1 * t + c2 * t * t) / (1.0 + d1 * t + d2 * t * t + d3 * t * t * t)
    return round(sign * z, 4)


# ---------------------------------------------------------------------------
# 1. Expected Utility (tier 5)
# ---------------------------------------------------------------------------

@register
class ExpectedUtilityGenerator(StepGenerator):
    """Compute expected utility of a lottery.

    Given a lottery with outcomes and probabilities and a utility
    function (sqrt, log, or linear), compute EU = sum p_i * u(x_i).

    Difficulty scaling:
        Difficulty 1-3: 2-3 outcomes, linear or sqrt utility.
        Difficulty 4-6: 3-4 outcomes, sqrt or log utility.
        Difficulty 7-8: 4-5 outcomes, log utility.

    Prerequisites:
        expected_value.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "expected_utility"

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
        return "compute expected utility of a lottery"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an expected utility problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 3)
            util_name = self._rng.choice(["linear", "sqrt"])
        elif difficulty <= 6:
            n = self._rng.randint(3, 4)
            util_name = self._rng.choice(["sqrt", "log"])
        else:
            n = self._rng.randint(4, 5)
            util_name = "log"

        outcomes = sorted(
            [self._rng.randint(1, 50 * max(1, difficulty)) for _ in range(n)]
        )
        raw = [self._rng.randint(1, 20) for _ in range(n)]
        total = sum(raw)
        probs = [round(w / total, 4) for w in raw]
        probs[-1] = round(1.0 - sum(probs[:-1]), 4)

        if util_name == "linear":
            utilities = [round(float(x), 4) for x in outcomes]
        elif util_name == "sqrt":
            utilities = [round(math.sqrt(x), 4) for x in outcomes]
        else:
            utilities = [round(math.log(x), 4) for x in outcomes]

        eu = round(sum(p * u for p, u in zip(probs, utilities)), 4)

        out_str = ", ".join(f"({outcomes[i]}, p={probs[i]})" for i in range(n))
        problem = f"lottery: [{out_str}]; u(x) = {util_name}(x). EU?"
        return problem, {
            "outcomes": outcomes, "probs": probs,
            "util_name": util_name, "utilities": utilities, "eu": eu,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate EU computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing utility values and weighted sum.
        """
        steps = []
        for i, (x, u) in enumerate(zip(sd["outcomes"], sd["utilities"])):
            steps.append(f"u({x}) = {u}")
        terms = " + ".join(
            f"{p}*{u}" for p, u in zip(sd["probs"], sd["utilities"])
        )
        steps.append(f"EU = {terms} = {sd['eu']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the expected utility.

        Args:
            sd: Solution data dict.

        Returns:
            EU value as string.
        """
        return f"EU = {sd['eu']}"


# ---------------------------------------------------------------------------
# 2. Risk Dominance (tier 5)
# ---------------------------------------------------------------------------

@register
class RiskDominanceGenerator(StepGenerator):
    """Check risk dominance between two strategies in a 2x2 game.

    Strategy A risk-dominates B if A yields higher expected utility
    when the opponent plays each strategy with probability 0.5.

    Difficulty scaling:
        Difficulty 1-4: simple payoffs in [0, 10].
        Difficulty 5-8: payoffs in [-5, 20].

    Prerequisites:
        nash_equilibrium.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "risk_dominance"

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
        return "determine which strategy risk-dominates"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a risk dominance problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        lo = -5 if difficulty >= 5 else 0
        hi = 20 if difficulty >= 5 else 10
        m = [
            [(self._rng.randint(lo, hi), self._rng.randint(lo, hi))
             for _ in range(2)]
            for _ in range(2)
        ]
        # Row player EU when opponent mixes 50/50
        eu_row0 = round(0.5 * m[0][0][0] + 0.5 * m[0][1][0], 4)
        eu_row1 = round(0.5 * m[1][0][0] + 0.5 * m[1][1][0], 4)

        if eu_row0 > eu_row1:
            dominant = "row 0"
        elif eu_row1 > eu_row0:
            dominant = "row 1"
        else:
            dominant = "neither"

        mat_str = (
            f"[({m[0][0][0]},{m[0][0][1]}),({m[0][1][0]},{m[0][1][1]})];"
            f"[({m[1][0][0]},{m[1][0][1]}),({m[1][1][0]},{m[1][1][1]})]"
        )
        return (
            f"risk dominance? matrix: {mat_str}",
            {
                "matrix": m, "eu_row0": eu_row0,
                "eu_row1": eu_row1, "dominant": dominant,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate risk dominance analysis steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing EU comparison at 50/50 mixing.
        """
        m = sd["matrix"]
        return [
            f"EU(row 0) = 0.5*{m[0][0][0]} + 0.5*{m[0][1][0]} = {sd['eu_row0']}",
            f"EU(row 1) = 0.5*{m[1][0][0]} + 0.5*{m[1][1][0]} = {sd['eu_row1']}",
            f"risk-dominant: {sd['dominant']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the risk-dominant strategy.

        Args:
            sd: Solution data dict.

        Returns:
            Which strategy risk-dominates.
        """
        return sd["dominant"]


# ---------------------------------------------------------------------------
# 3. Bayesian Updating (tier 6)
# ---------------------------------------------------------------------------

@register
class BayesianUpdatingGenerator(StepGenerator):
    """Perform Bayesian updating on a hypothesis.

    Given prior P(H), likelihood P(E|H), and P(E|not H), compute
    posterior P(H|E) via Bayes' theorem. At high difficulty, perform
    multi-step updating with sequential evidence.

    Difficulty scaling:
        Difficulty 1-4: single update.
        Difficulty 5-8: 2-3 sequential updates.

    Prerequisites:
        bayes_theorem.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bayesian_updating"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bayes_theorem"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "Bayesian update: compute posterior from prior and likelihood"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Bayesian updating problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_updates = 1 if difficulty <= 4 else self._rng.randint(2, 3)
        prior = round(self._rng.uniform(0.1, 0.9), 2)

        updates = []
        current = prior
        for _ in range(n_updates):
            p_e_h = round(self._rng.uniform(0.2, 0.95), 2)
            p_e_nh = round(self._rng.uniform(0.05, 0.6), 2)
            p_e = round(p_e_h * current + p_e_nh * (1.0 - current), 4)
            if p_e == 0.0:
                p_e = 0.0001
            posterior = round(p_e_h * current / p_e, 4)
            updates.append({
                "p_e_h": p_e_h, "p_e_nh": p_e_nh,
                "p_e": p_e, "prior": round(current, 4),
                "posterior": posterior,
            })
            current = posterior

        evidence_str = "; ".join(
            f"E{i+1}: P(E|H)={u['p_e_h']}, P(E|~H)={u['p_e_nh']}"
            for i, u in enumerate(updates)
        )
        problem = f"prior P(H)={prior}; {evidence_str}. posterior?"
        return problem, {
            "prior": prior, "updates": updates,
            "final_posterior": updates[-1]["posterior"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Bayesian updating steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing each update application.
        """
        steps = [f"prior = {sd['prior']}"]
        for i, u in enumerate(sd["updates"]):
            steps.append(
                f"P(E{i+1}) = {u['p_e_h']}*{u['prior']} + "
                f"{u['p_e_nh']}*{round(1.0 - u['prior'], 4)} = {u['p_e']}"
            )
            steps.append(
                f"P(H|E{i+1}) = {u['p_e_h']}*{u['prior']}/{u['p_e']} "
                f"= {u['posterior']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final posterior probability.

        Args:
            sd: Solution data dict.

        Returns:
            Posterior P(H|E) as string.
        """
        return f"P(H|E) = {sd['final_posterior']}"


# ---------------------------------------------------------------------------
# 4. Value of Information (tier 6)
# ---------------------------------------------------------------------------

@register
class ValueOfInformationGenerator(StepGenerator):
    """Compute value of information for a simple decision tree.

    VoI = EU(with information) - EU(without information).
    Binary signal with known accuracy on a binary state.

    Difficulty scaling:
        Difficulty 1-4: symmetric signal accuracy.
        Difficulty 5-8: asymmetric signal (different true-positive/false-positive).

    Prerequisites:
        bayesian_updating.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "value_of_information"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bayesian_updating"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute value of information for binary decision"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a value of information problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        prior = round(self._rng.uniform(0.2, 0.8), 2)
        payoff_h = self._rng.randint(10, 50 * max(1, difficulty))
        payoff_nh = self._rng.randint(-30 * max(1, difficulty), -1)

        if difficulty <= 4:
            accuracy = round(self._rng.uniform(0.6, 0.95), 2)
            tp = accuracy
            fp = round(1.0 - accuracy, 4)
        else:
            tp = round(self._rng.uniform(0.6, 0.95), 2)
            fp = round(self._rng.uniform(0.05, 0.4), 2)

        # EU without info: max(prior*payoff_h + (1-prior)*payoff_nh, 0)
        eu_act = round(prior * payoff_h + (1.0 - prior) * payoff_nh, 4)
        eu_no_info = round(max(eu_act, 0.0), 4)

        # P(signal positive)
        p_pos = round(tp * prior + fp * (1.0 - prior), 4)
        p_neg = round(1.0 - p_pos, 4)

        # Posterior given positive signal
        post_pos = round(tp * prior / p_pos, 4) if p_pos > 0 else 0.0
        # Posterior given negative signal
        tn = round(1.0 - fp, 4)
        fn = round(1.0 - tp, 4)
        post_neg = round(fn * prior / p_neg, 4) if p_neg > 0 else 0.0

        # EU with info
        eu_pos = round(post_pos * payoff_h + (1.0 - post_pos) * payoff_nh, 4)
        eu_neg = round(post_neg * payoff_h + (1.0 - post_neg) * payoff_nh, 4)
        eu_with_info = round(
            p_pos * max(eu_pos, 0.0) + p_neg * max(eu_neg, 0.0), 4
        )

        voi = round(eu_with_info - eu_no_info, 4)

        problem = (
            f"prior={prior}, payoff(H)={payoff_h}, payoff(~H)={payoff_nh}, "
            f"TP={tp}, FP={fp}. VoI?"
        )
        return problem, {
            "prior": prior, "payoff_h": payoff_h, "payoff_nh": payoff_nh,
            "tp": tp, "fp": fp, "eu_no_info": eu_no_info,
            "p_pos": p_pos, "p_neg": p_neg,
            "post_pos": post_pos, "post_neg": post_neg,
            "eu_pos": eu_pos, "eu_neg": eu_neg,
            "eu_with_info": eu_with_info, "voi": voi,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate VoI computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing decision tree evaluation.
        """
        return [
            f"EU(act) = {sd['prior']}*{sd['payoff_h']} + "
            f"{round(1.0 - sd['prior'], 4)}*{sd['payoff_nh']} = "
            f"{round(sd['prior'] * sd['payoff_h'] + (1.0 - sd['prior']) * sd['payoff_nh'], 4)}",
            f"EU(no info) = max(EU(act), 0) = {sd['eu_no_info']}",
            f"P(+) = {sd['p_pos']}, P(-) = {sd['p_neg']}",
            f"P(H|+) = {sd['post_pos']}, P(H|-) = {sd['post_neg']}",
            f"EU(with info) = {sd['eu_with_info']}",
            f"VoI = {sd['eu_with_info']} - {sd['eu_no_info']} = {sd['voi']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the value of information.

        Args:
            sd: Solution data dict.

        Returns:
            VoI as string.
        """
        return f"VoI = {sd['voi']}"


# ---------------------------------------------------------------------------
# 5. Multi-Criteria Decision Making (tier 5)
# ---------------------------------------------------------------------------

@register
class MultiCriteriaGenerator(StepGenerator):
    """Weighted scoring for multi-criteria decision making.

    Compute score = sum w_i * s_i for n alternatives on m criteria,
    then rank the alternatives by total score.

    Difficulty scaling:
        Difficulty 1-3: 2 alternatives, 2-3 criteria.
        Difficulty 4-6: 3 alternatives, 3-4 criteria.
        Difficulty 7-8: 4 alternatives, 4-5 criteria.

    Prerequisites:
        weighted_sum.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "multi_criteria"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["weighted_sum"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "rank alternatives by weighted multi-criteria scoring"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a multi-criteria decision problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_alt = 2
            n_crit = self._rng.randint(2, 3)
        elif difficulty <= 6:
            n_alt = 3
            n_crit = self._rng.randint(3, 4)
        else:
            n_alt = 4
            n_crit = self._rng.randint(4, 5)

        raw_w = [self._rng.randint(1, 10) for _ in range(n_crit)]
        total_w = sum(raw_w)
        weights = [round(w / total_w, 4) for w in raw_w]
        weights[-1] = round(1.0 - sum(weights[:-1]), 4)

        scores = [
            [self._rng.randint(1, 10) for _ in range(n_crit)]
            for _ in range(n_alt)
        ]

        totals = [
            round(sum(w * s for w, s in zip(weights, alt_scores)), 4)
            for alt_scores in scores
        ]

        ranking = sorted(range(n_alt), key=lambda i: totals[i], reverse=True)
        labels = [chr(ord("A") + i) for i in range(n_alt)]

        w_str = ", ".join(f"w{j+1}={weights[j]}" for j in range(n_crit))
        alt_strs = "; ".join(
            f"{labels[i]}=[" + ",".join(str(s) for s in scores[i]) + "]"
            for i in range(n_alt)
        )
        problem = f"weights: [{w_str}]; {alt_strs}. rank?"
        return problem, {
            "weights": weights, "scores": scores, "totals": totals,
            "ranking": ranking, "labels": labels,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate multi-criteria scoring steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing each alternative's weighted score.
        """
        steps = []
        for i, (label, alt_scores) in enumerate(
            zip(sd["labels"], sd["scores"])
        ):
            terms = " + ".join(
                f"{w}*{s}" for w, s in zip(sd["weights"], alt_scores)
            )
            steps.append(f"{label}: {terms} = {sd['totals'][i]}")
        rank_str = " > ".join(
            sd["labels"][i] for i in sd["ranking"]
        )
        steps.append(f"ranking: {rank_str}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the ranking of alternatives.

        Args:
            sd: Solution data dict.

        Returns:
            Ranked alternatives as string.
        """
        return " > ".join(sd["labels"][i] for i in sd["ranking"])


# ---------------------------------------------------------------------------
# 6. Prospect Theory (tier 6)
# ---------------------------------------------------------------------------

@register
class ProspectTheoryGenerator(StepGenerator):
    """Compute prospect value using Kahneman-Tversky value and weight functions.

    v(x) = x^0.88 for gains, -2.25*(-x)^0.88 for losses.
    w(p) = p^0.65 / (p^0.65 + (1-p)^0.65)^(1/0.65).
    Prospect value = sum w(p_i) * v(x_i).

    Difficulty scaling:
        Difficulty 1-3: 2 outcomes, all gains or all losses.
        Difficulty 4-6: 2-3 outcomes, mixed gains/losses.
        Difficulty 7-8: 3-4 outcomes, mixed gains/losses.

    Prerequisites:
        expected_utility.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "prospect_theory"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["expected_utility"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute prospect value with KT value and weight functions"

    @staticmethod
    def _value_fn(x: float) -> float:
        """Kahneman-Tversky value function.

        Args:
            x: Outcome amount (positive=gain, negative=loss).

        Returns:
            Subjective value.
        """
        if x >= 0:
            return round(x ** 0.88, 4)
        return round(-2.25 * ((-x) ** 0.88), 4)

    @staticmethod
    def _weight_fn(p: float) -> float:
        """Kahneman-Tversky probability weighting function.

        Args:
            p: Objective probability in (0, 1).

        Returns:
            Decision weight.
        """
        if p <= 0.0:
            return 0.0
        if p >= 1.0:
            return 1.0
        p_g = p ** 0.65
        q_g = (1.0 - p) ** 0.65
        return round(p_g / (p_g + q_g) ** (1.0 / 0.65), 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a prospect theory computation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 2
            if self._rng.random() < 0.5:
                outcomes = [self._rng.randint(5, 100) for _ in range(n)]
            else:
                outcomes = [-self._rng.randint(5, 100) for _ in range(n)]
        elif difficulty <= 6:
            n = self._rng.randint(2, 3)
            outcomes = [
                self._rng.randint(-80, 80) for _ in range(n)
            ]
            # Ensure at least one gain and one loss
            if all(x >= 0 for x in outcomes):
                outcomes[0] = -self._rng.randint(5, 50)
            if all(x < 0 for x in outcomes):
                outcomes[0] = self._rng.randint(5, 50)
        else:
            n = self._rng.randint(3, 4)
            outcomes = [
                self._rng.randint(-100, 100) for _ in range(n)
            ]
            if all(x >= 0 for x in outcomes):
                outcomes[0] = -self._rng.randint(5, 50)
            if all(x < 0 for x in outcomes):
                outcomes[0] = self._rng.randint(5, 50)

        # Avoid zero outcomes for cleaner arithmetic
        outcomes = [x if x != 0 else 1 for x in outcomes]

        raw = [self._rng.randint(1, 20) for _ in range(n)]
        total = sum(raw)
        probs = [round(w / total, 4) for w in raw]
        probs[-1] = round(1.0 - sum(probs[:-1]), 4)

        values = [self._value_fn(x) for x in outcomes]
        weights = [self._weight_fn(p) for p in probs]
        pv = round(sum(w * v for w, v in zip(weights, values)), 4)

        out_str = ", ".join(
            f"({outcomes[i]}, p={probs[i]})" for i in range(n)
        )
        problem = f"prospect: [{out_str}]. compute prospect value"
        return problem, {
            "outcomes": outcomes, "probs": probs,
            "values": values, "weights": weights, "pv": pv,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate prospect theory computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing value function, weight function, and total.
        """
        steps = []
        for i, x in enumerate(sd["outcomes"]):
            steps.append(f"v({x}) = {sd['values'][i]}")
        for i, p in enumerate(sd["probs"]):
            steps.append(f"w({p}) = {sd['weights'][i]}")
        terms = " + ".join(
            f"{sd['weights'][i]}*{sd['values'][i]}"
            for i in range(len(sd["outcomes"]))
        )
        steps.append(f"PV = {terms} = {sd['pv']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the prospect value.

        Args:
            sd: Solution data dict.

        Returns:
            Prospect value as string.
        """
        return f"PV = {sd['pv']}"


# ---------------------------------------------------------------------------
# 7. Sequential Decision (tier 6)
# ---------------------------------------------------------------------------

@register
class SequentialDecisionGenerator(StepGenerator):
    """Solve a 2-3 stage decision tree by backward induction.

    At each decision node choose the action maximising expected
    utility. Chance nodes have given probabilities.

    Difficulty scaling:
        Difficulty 1-4: 2-stage tree (1 decision, 1 chance node).
        Difficulty 5-8: 3-stage tree (2 decisions, chance nodes).

    Prerequisites:
        minimax.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sequential_decision"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "solve decision tree by backward induction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sequential decision tree problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        stages = 2 if difficulty <= 4 else 3

        if stages == 2:
            # Decision: action A or B, then chance with 2 outcomes each
            p = round(self._rng.uniform(0.2, 0.8), 2)
            payoffs_a = [self._rng.randint(-20, 50), self._rng.randint(-20, 50)]
            payoffs_b = [self._rng.randint(-20, 50), self._rng.randint(-20, 50)]
            eu_a = round(p * payoffs_a[0] + (1.0 - p) * payoffs_a[1], 4)
            eu_b = round(p * payoffs_b[0] + (1.0 - p) * payoffs_b[1], 4)
            best = "A" if eu_a >= eu_b else "B"
            opt_eu = round(max(eu_a, eu_b), 4)
            problem = (
                f"2-stage: p(s1)={p}; "
                f"A->[{payoffs_a[0]},{payoffs_a[1]}], "
                f"B->[{payoffs_b[0]},{payoffs_b[1]}]. optimal?"
            )
            return problem, {
                "stages": 2, "p": p,
                "payoffs_a": payoffs_a, "payoffs_b": payoffs_b,
                "eu_a": eu_a, "eu_b": eu_b,
                "best": best, "opt_eu": opt_eu,
            }
        else:
            # Stage 1: choose A or B
            # Stage 2: chance with prob p, then choose C or D at each outcome
            p = round(self._rng.uniform(0.3, 0.7), 2)
            # Payoffs for A path: under s1 choose C/D, under s2 choose C/D
            a_s1_c = self._rng.randint(-10, 40)
            a_s1_d = self._rng.randint(-10, 40)
            a_s2_c = self._rng.randint(-10, 40)
            a_s2_d = self._rng.randint(-10, 40)
            # Payoffs for B path
            b_s1_c = self._rng.randint(-10, 40)
            b_s1_d = self._rng.randint(-10, 40)
            b_s2_c = self._rng.randint(-10, 40)
            b_s2_d = self._rng.randint(-10, 40)

            # Backward induction
            best_a_s1 = max(a_s1_c, a_s1_d)
            best_a_s2 = max(a_s2_c, a_s2_d)
            best_b_s1 = max(b_s1_c, b_s1_d)
            best_b_s2 = max(b_s2_c, b_s2_d)

            eu_a = round(p * best_a_s1 + (1.0 - p) * best_a_s2, 4)
            eu_b = round(p * best_b_s1 + (1.0 - p) * best_b_s2, 4)
            best = "A" if eu_a >= eu_b else "B"
            opt_eu = round(max(eu_a, eu_b), 4)

            problem = (
                f"3-stage: p(s1)={p}; "
                f"A-s1:[C={a_s1_c},D={a_s1_d}], A-s2:[C={a_s2_c},D={a_s2_d}]; "
                f"B-s1:[C={b_s1_c},D={b_s1_d}], B-s2:[C={b_s2_c},D={b_s2_d}]"
            )
            return problem, {
                "stages": 3, "p": p,
                "a_s1_c": a_s1_c, "a_s1_d": a_s1_d,
                "a_s2_c": a_s2_c, "a_s2_d": a_s2_d,
                "b_s1_c": b_s1_c, "b_s1_d": b_s1_d,
                "b_s2_c": b_s2_c, "b_s2_d": b_s2_d,
                "best_a_s1": best_a_s1, "best_a_s2": best_a_s2,
                "best_b_s1": best_b_s1, "best_b_s2": best_b_s2,
                "eu_a": eu_a, "eu_b": eu_b,
                "best": best, "opt_eu": opt_eu,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate backward induction steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing value propagation from leaves to root.
        """
        if sd["stages"] == 2:
            return [
                f"EU(A) = {sd['p']}*{sd['payoffs_a'][0]} + "
                f"{round(1.0 - sd['p'], 4)}*{sd['payoffs_a'][1]} = {sd['eu_a']}",
                f"EU(B) = {sd['p']}*{sd['payoffs_b'][0]} + "
                f"{round(1.0 - sd['p'], 4)}*{sd['payoffs_b'][1]} = {sd['eu_b']}",
                f"optimal: {sd['best']}, EU = {sd['opt_eu']}",
            ]
        return [
            f"A-s1: max({sd['a_s1_c']},{sd['a_s1_d']}) = {sd['best_a_s1']}",
            f"A-s2: max({sd['a_s2_c']},{sd['a_s2_d']}) = {sd['best_a_s2']}",
            f"EU(A) = {sd['p']}*{sd['best_a_s1']} + "
            f"{round(1.0 - sd['p'], 4)}*{sd['best_a_s2']} = {sd['eu_a']}",
            f"B-s1: max({sd['b_s1_c']},{sd['b_s1_d']}) = {sd['best_b_s1']}",
            f"B-s2: max({sd['b_s2_c']},{sd['b_s2_d']}) = {sd['best_b_s2']}",
            f"EU(B) = {sd['p']}*{sd['best_b_s1']} + "
            f"{round(1.0 - sd['p'], 4)}*{sd['best_b_s2']} = {sd['eu_b']}",
            f"optimal: {sd['best']}, EU = {sd['opt_eu']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the optimal decision and EU.

        Args:
            sd: Solution data dict.

        Returns:
            Best action and expected utility.
        """
        return f"{sd['best']}, EU = {sd['opt_eu']}"


# ---------------------------------------------------------------------------
# 8. Mechanism Design / VCG (tier 7)
# ---------------------------------------------------------------------------

@register
class MechanismDesignGenerator(StepGenerator):
    """Compute VCG payments for a multi-bidder auction.

    Each agent's VCG payment = externality they impose on others:
    payment_i = max welfare(others without i) - welfare(others with i).

    Difficulty scaling:
        Difficulty 1-4: 2 bidders, 1 item.
        Difficulty 5-8: 3 bidders, 1 item.

    Prerequisites:
        auction_revenue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mechanism_design"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["auction_revenue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute VCG payments for single-item auction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a VCG mechanism design problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 2 if difficulty <= 4 else 3
        bids = sorted(
            [self._rng.randint(1, 20 * max(1, difficulty)) for _ in range(n)],
            reverse=True,
        )

        # Winner is highest bidder (index 0 after sorting)
        winner = 0
        # VCG payment for winner = welfare of others without winner
        # minus welfare of others with winner present
        # Without winner: second-highest bidder wins, gets bids[1] welfare
        # With winner: others get 0 (single item)
        vcg_payment = bids[1]  # second-highest bid

        # Non-winners pay 0 (they don't get the item)
        payments = [0] * n
        payments[winner] = vcg_payment

        bid_str = ", ".join(f"b{i+1}={bids[i]}" for i in range(n))
        problem = f"VCG auction: {n} bidders, 1 item; {bid_str}. payments?"
        return problem, {
            "n": n, "bids": bids, "winner": winner,
            "vcg_payment": vcg_payment, "payments": payments,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate VCG payment computation steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing externality calculation.
        """
        steps = [
            f"bids (sorted): {sd['bids']}",
            f"winner: bidder 1 (bid={sd['bids'][0]})",
            f"welfare(others w/o winner) = {sd['bids'][1]}",
            f"welfare(others w/ winner) = 0",
            f"payment(winner) = {sd['bids'][1]} - 0 = {sd['vcg_payment']}",
        ]
        for i in range(1, sd["n"]):
            steps.append(f"payment(bidder {i+1}) = 0 (non-winner)")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the VCG payments.

        Args:
            sd: Solution data dict.

        Returns:
            Payments for each bidder.
        """
        pay_str = ", ".join(
            f"b{i+1}={sd['payments'][i]}" for i in range(sd["n"])
        )
        return f"payments: [{pay_str}]"
