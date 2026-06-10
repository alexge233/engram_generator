"""Reinforcement learning extension generators -- TD(lambda), SARSA, REINFORCE, UCB.

4 generators across tiers 5-6 covering temporal difference learning,
on-policy SARSA updates, policy gradient estimation, and multi-armed
bandit action selection via upper confidence bounds.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. TD(lambda) Update
# ---------------------------------------------------------------------------

@register
class TDLambdaGenerator(StepGenerator):
    """Compute a TD(0) value update with optional eligibility traces.

    Applies V(s) = V(s) + alpha * (R + gamma * V(s') - V(s)) to a
    given transition. At high difficulty, introduces eligibility traces
    that decay by gamma * lambda each step.

    Difficulty scaling:
        Difficulty 1-3: 3 states, single transition, no traces.
        Difficulty 4-6: 4-5 states, single transition, no traces.
        Difficulty 7-8: 5-6 states, 2-step trajectory with eligibility traces.

    Prerequisites:
        bellman_equation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "td_lambda"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["bellman_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute TD update with eligibility traces"
        return "compute TD(0) value update for a transition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a TD update problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_states = min(3 + difficulty // 2, 6)
        values = [round(self._rng.uniform(0.0, 5.0), 2) for _ in range(n_states)]
        alpha = round(self._rng.choice([0.05, 0.1, 0.2, 0.3]), 2)
        gamma = round(self._rng.choice([0.9, 0.95, 0.99]), 2)

        s = self._rng.randint(0, n_states - 1)
        s_next = self._rng.randint(0, n_states - 1)
        reward = round(self._rng.uniform(-2.0, 5.0), 2)

        td_target = round(reward + gamma * values[s_next], 4)
        td_error = round(td_target - values[s], 4)
        new_v = round(values[s] + alpha * td_error, 4)

        data = {
            "values": values, "alpha": alpha, "gamma": gamma,
            "s": s, "s_next": s_next, "reward": reward,
            "td_target": td_target, "td_error": td_error,
            "new_v": new_v, "use_traces": False,
        }

        if difficulty >= 7:
            lam = round(self._rng.choice([0.5, 0.7, 0.8, 0.9]), 2)
            s2 = self._rng.randint(0, n_states - 1)
            r2 = round(self._rng.uniform(-1.0, 3.0), 2)
            trace_s = round(gamma * lam * 1.0, 4)
            td_target2 = round(r2 + gamma * values[s2], 4)
            td_error2 = round(td_target2 - values[s_next], 4)
            v_s_update2 = round(new_v + alpha * td_error2 * trace_s, 4)
            data.update({
                "use_traces": True, "lam": lam,
                "s2": s2, "r2": r2,
                "trace_s": trace_s, "td_error2": td_error2,
                "v_s_update2": v_s_update2,
            })

        v_str = ", ".join(f"V({i})={v}" for i, v in enumerate(values))
        problem = (
            f"TD: {v_str}, alpha={alpha}, gamma={gamma}, "
            f"transition s={s},R={reward},s'={s_next}"
        )
        if difficulty >= 7:
            problem += f", lam={data['lam']}, then s'={s_next},R={data['r2']},s''={data['s2']}"
        return problem, data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for the TD update.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the TD computation.
        """
        steps = [
            f"TD target = R + gamma*V(s') = {data['reward']} + "
            f"{data['gamma']}*{data['values'][data['s_next']]} = {data['td_target']}",
            f"TD error = {data['td_target']} - V({data['s']}) = "
            f"{data['td_target']} - {data['values'][data['s']]} = {data['td_error']}",
            f"V({data['s']}) = {data['values'][data['s']]} + "
            f"{data['alpha']}*{data['td_error']} = {data['new_v']}",
        ]
        if data["use_traces"]:
            steps.append(
                f"trace(s={data['s']}) = gamma*lam = "
                f"{data['gamma']}*{data['lam']} = {data['trace_s']}"
            )
            steps.append(
                f"V({data['s']}) += alpha*delta2*trace = "
                f"{data['alpha']}*{data['td_error2']}*{data['trace_s']} "
                f"=> V({data['s']}) = {data['v_s_update2']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the updated value.

        Args:
            data: Solution data dict.

        Returns:
            Updated value as a string.
        """
        if data["use_traces"]:
            return f"V({data['s']}) = {data['v_s_update2']}"
        return f"V({data['s']}) = {data['new_v']}"


# ---------------------------------------------------------------------------
# 2. SARSA Update
# ---------------------------------------------------------------------------

@register
class SARSAUpdateGenerator(StepGenerator):
    """Compute an on-policy SARSA Q-value update.

    Applies Q(s,a) = Q(s,a) + alpha * (R + gamma * Q(s',a') - Q(s,a)).
    Also computes the off-policy Q-learning alternative using max over
    actions to show the difference.

    Difficulty scaling:
        Difficulty 1-3: 2 states, 2 actions.
        Difficulty 4-6: 3 states, 3 actions.
        Difficulty 7-8: 4 states, 4 actions.

    Prerequisites:
        q_value_update.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sarsa_update"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["q_value_update"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute SARSA update and compare with Q-learning"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a SARSA update problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_states = min(2 + (difficulty - 1) // 2, 4)
        n_actions = min(2 + (difficulty - 1) // 2, 4)

        q_table = [
            [round(self._rng.uniform(-1.0, 3.0), 2)
             for _ in range(n_actions)]
            for _ in range(n_states)
        ]
        alpha = round(self._rng.choice([0.1, 0.2, 0.3]), 2)
        gamma = round(self._rng.choice([0.9, 0.95, 0.99]), 2)

        s = self._rng.randint(0, n_states - 1)
        a = self._rng.randint(0, n_actions - 1)
        s_next = self._rng.randint(0, n_states - 1)
        a_next = self._rng.randint(0, n_actions - 1)
        reward = round(self._rng.uniform(-1.0, 5.0), 2)

        q_sa = q_table[s][a]
        q_sa_next = q_table[s_next][a_next]
        sarsa_target = round(reward + gamma * q_sa_next, 4)
        sarsa_error = round(sarsa_target - q_sa, 4)
        sarsa_new = round(q_sa + alpha * sarsa_error, 4)

        q_max = max(q_table[s_next])
        ql_target = round(reward + gamma * q_max, 4)
        ql_error = round(ql_target - q_sa, 4)
        ql_new = round(q_sa + alpha * ql_error, 4)

        q_str = "; ".join(
            f"Q({si},{ai})={q_table[si][ai]}"
            for si in range(n_states)
            for ai in range(n_actions)
        )
        problem = (
            f"SARSA: {q_str}, alpha={alpha}, gamma={gamma}, "
            f"(s={s},a={a},R={reward},s'={s_next},a'={a_next})"
        )
        return problem, {
            "q_table": q_table, "alpha": alpha, "gamma": gamma,
            "s": s, "a": a, "s_next": s_next, "a_next": a_next,
            "reward": reward, "q_sa": q_sa, "q_sa_next": q_sa_next,
            "sarsa_target": sarsa_target, "sarsa_error": sarsa_error,
            "sarsa_new": sarsa_new,
            "q_max": q_max, "ql_target": ql_target,
            "ql_error": ql_error, "ql_new": ql_new,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for SARSA.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing SARSA and Q-learning comparison.
        """
        return [
            f"SARSA target = R + gamma*Q(s',a') = {data['reward']} + "
            f"{data['gamma']}*{data['q_sa_next']} = {data['sarsa_target']}",
            f"SARSA error = {data['sarsa_target']} - {data['q_sa']} = "
            f"{data['sarsa_error']}",
            f"Q_SARSA({data['s']},{data['a']}) = {data['q_sa']} + "
            f"{data['alpha']}*{data['sarsa_error']} = {data['sarsa_new']}",
            f"Q-learn: max Q(s',.) = {data['q_max']}, "
            f"target = {data['ql_target']}, "
            f"Q_QL({data['s']},{data['a']}) = {data['ql_new']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the SARSA-updated Q-value.

        Args:
            data: Solution data dict.

        Returns:
            Updated Q-value as a string.
        """
        return (
            f"SARSA: Q({data['s']},{data['a']}) = {data['sarsa_new']}, "
            f"Q-learn: {data['ql_new']}"
        )


# ---------------------------------------------------------------------------
# 3. Policy Gradient (REINFORCE)
# ---------------------------------------------------------------------------

@register
class PolicyGradientReinforceGenerator(StepGenerator):
    """Compute REINFORCE policy gradient direction from a trajectory.

    Given a trajectory of (state, action, reward) tuples and action
    probabilities, computes the discounted return G_t for each step
    and the gradient direction: positive for taken actions weighted by
    G_t, negative for others.

    Difficulty scaling:
        Difficulty 1-3: 2-step trajectory, 2 actions.
        Difficulty 4-6: 3-step trajectory, 2-3 actions.
        Difficulty 7-8: 4-step trajectory, 3 actions.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "policy_gradient_reinforce"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute REINFORCE policy gradient from trajectory"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a REINFORCE gradient computation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_steps = min(2 + (difficulty - 1) // 2, 4)
        n_actions = 2 if difficulty <= 4 else 3
        gamma = round(self._rng.choice([0.9, 0.95, 0.99]), 2)

        rewards = [round(self._rng.uniform(-1.0, 5.0), 2)
                   for _ in range(n_steps)]
        actions = [self._rng.randint(0, n_actions - 1)
                   for _ in range(n_steps)]
        probs = []
        for _ in range(n_steps):
            raw = [self._rng.uniform(0.1, 1.0) for _ in range(n_actions)]
            total = sum(raw)
            p = [round(x / total, 4) for x in raw]
            diff = round(1.0 - sum(p), 4)
            p[-1] = round(p[-1] + diff, 4)
            probs.append(p)

        returns = [0.0] * n_steps
        returns[-1] = rewards[-1]
        for t in range(n_steps - 2, -1, -1):
            returns[t] = round(rewards[t] + gamma * returns[t + 1], 4)

        log_probs = []
        for t in range(n_steps):
            lp = round(math.log(max(probs[t][actions[t]], 1e-8)), 4)
            log_probs.append(lp)

        grad_terms = [round(log_probs[t] * returns[t], 4)
                      for t in range(n_steps)]
        grad_sum = round(sum(grad_terms), 4)

        traj_str = ", ".join(
            f"(a={actions[t]},r={rewards[t]},pi={probs[t]})"
            for t in range(n_steps)
        )
        problem = f"REINFORCE: gamma={gamma}, trajectory: {traj_str}"
        return problem, {
            "gamma": gamma, "rewards": rewards, "actions": actions,
            "probs": probs, "returns": returns, "log_probs": log_probs,
            "grad_terms": grad_terms, "grad_sum": grad_sum,
            "n_steps": n_steps,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for REINFORCE.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing return and gradient computation.
        """
        steps = []
        for t in range(data["n_steps"] - 1, -1, -1):
            if t == data["n_steps"] - 1:
                steps.append(f"G_{t} = r_{t} = {data['rewards'][t]}")
            else:
                steps.append(
                    f"G_{t} = r_{t} + gamma*G_{t+1} = {data['rewards'][t]} + "
                    f"{data['gamma']}*{data['returns'][t+1]} = {data['returns'][t]}"
                )
        for t in range(data["n_steps"]):
            steps.append(
                f"log pi(a_{t}|s_{t}) * G_{t} = "
                f"{data['log_probs'][t]} * {data['returns'][t]} = "
                f"{data['grad_terms'][t]}"
            )
        steps.append(f"grad J = sum = {data['grad_sum']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the gradient sum.

        Args:
            data: Solution data dict.

        Returns:
            Total gradient as a string.
        """
        return f"grad J = {data['grad_sum']}"


# ---------------------------------------------------------------------------
# 4. Bandit UCB1
# ---------------------------------------------------------------------------

@register
class BanditUCBGenerator(StepGenerator):
    """Select an action using UCB1 and compute regret.

    Applies UCB1: a* = argmax(Q(a) + c * sqrt(ln(t) / N(a))) where
    Q(a) is the estimated value, N(a) is the pull count, and t is the
    total number of pulls. Also computes simple regret as the
    difference between the best true mean and the selected action's
    true mean.

    Difficulty scaling:
        Difficulty 1-3: 2-3 arms, t < 20.
        Difficulty 4-6: 3-4 arms, t < 50.
        Difficulty 7-8: 4-5 arms, t < 100.

    Prerequisites:
        expected_value.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bandit_ucb"

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
        return "select action using UCB1 and compute regret"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a UCB1 action selection problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_arms = min(2 + (difficulty - 1) // 2, 5)
        t_cap = 20 if difficulty <= 3 else (50 if difficulty <= 6 else 100)
        c = round(self._rng.choice([1.0, 1.41, 2.0]), 2)

        q_values = [round(self._rng.uniform(0.5, 4.0), 2)
                    for _ in range(n_arms)]
        counts = [self._rng.randint(1, max(2, t_cap // n_arms))
                  for _ in range(n_arms)]
        t = sum(counts)
        true_means = [round(self._rng.uniform(0.5, 5.0), 2)
                      for _ in range(n_arms)]

        ln_t = round(math.log(t), 4)
        ucb_values = []
        for i in range(n_arms):
            bonus = round(c * math.sqrt(ln_t / counts[i]), 4)
            ucb = round(q_values[i] + bonus, 4)
            ucb_values.append({"bonus": bonus, "ucb": ucb})

        best_arm = max(range(n_arms), key=lambda i: ucb_values[i]["ucb"])
        best_true = max(true_means)
        regret = round(best_true - true_means[best_arm], 4)

        q_str = ", ".join(f"Q({i})={q_values[i]}" for i in range(n_arms))
        n_str = ", ".join(f"N({i})={counts[i]}" for i in range(n_arms))
        problem = f"UCB1: {q_str}, {n_str}, c={c}, t={t}"
        return problem, {
            "n_arms": n_arms, "q_values": q_values, "counts": counts,
            "t": t, "c": c, "ln_t": ln_t, "ucb_values": ucb_values,
            "best_arm": best_arm, "true_means": true_means,
            "best_true": best_true, "regret": regret,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for UCB1.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing UCB computation and action selection.
        """
        steps = [f"ln(t) = ln({data['t']}) = {data['ln_t']}"]
        for i in range(data["n_arms"]):
            uv = data["ucb_values"][i]
            steps.append(
                f"UCB({i}) = {data['q_values'][i]} + "
                f"{data['c']}*sqrt({data['ln_t']}/{data['counts'][i]}) = "
                f"{data['q_values'][i]} + {uv['bonus']} = {uv['ucb']}"
            )
        steps.append(f"select a* = {data['best_arm']}")
        steps.append(
            f"regret = {data['best_true']} - "
            f"{data['true_means'][data['best_arm']]} = {data['regret']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the selected action and regret.

        Args:
            data: Solution data dict.

        Returns:
            Action and regret as a string.
        """
        return f"a* = {data['best_arm']}, regret = {data['regret']}"
