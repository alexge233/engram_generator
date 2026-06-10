"""Information geometry generators.

4 generators across tiers 6-7 covering Fisher information, natural
gradient, KL divergence geometry, and exponential family forms.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


@register
class FisherInformationGenerator(StepGenerator):
    """Compute the Fisher information matrix.

    Evaluates I(theta) = E[(d log f / d theta)^2] for common
    distributions: Bernoulli, Poisson, and Normal (1- or 2-parameter).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fisher_information"

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
        return "compute Fisher information matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fisher information problem.

        Args:
            difficulty: Controls distribution complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # Bernoulli: I(p) = 1 / (p*(1-p))
            p = round(self._rng.uniform(0.15, 0.85), 4)
            fisher = round(1.0 / (p * (1 - p)), 4)
            steps = [
                f"Bernoulli(p={p})",
                f"score = (x - p) / (p*(1-p))",
                f"I(p) = 1 / (p*(1-p)) = 1 / ({round(p * (1 - p), 4)})",
                f"I(p) = {fisher}",
            ]
            problem = f"Fisher information for Bernoulli(p={p})"
            return problem, {"fisher": fisher, "steps_log": steps}
        elif difficulty <= 5:
            # Poisson: I(lambda) = 1/lambda
            lam = round(self._rng.uniform(0.5, 8.0), 4)
            fisher = round(1.0 / lam, 4)
            steps = [
                f"Poisson(lambda={lam})",
                f"log f = x*log(lam) - lam - log(x!)",
                f"score = x/lam - 1, E[x] = lam",
                f"I(lam) = 1/lam = {fisher}",
            ]
            problem = f"Fisher information for Poisson(lam={lam})"
            return problem, {"fisher": fisher, "steps_log": steps}
        else:
            # Normal 2-parameter: I = diag(1/sigma^2, 2/sigma^2)
            mu = round(self._rng.uniform(-5.0, 5.0), 2)
            sigma = round(self._rng.uniform(0.5, 4.0), 4)
            s2 = sigma * sigma
            i_mu = round(1.0 / s2, 4)
            i_sig = round(2.0 / s2, 4)
            steps = [
                f"Normal(mu={mu}, sigma={sigma})",
                f"I_mu,mu = 1/sigma^2 = {i_mu}",
                f"I_sigma,sigma = 2/sigma^2 = {i_sig}",
                f"I = diag({i_mu}, {i_sig})",
            ]
            fisher_mat = [[i_mu, 0.0], [0.0, i_sig]]
            problem = f"Fisher info for Normal(mu={mu}, sigma={sigma})"
            return problem, {
                "fisher": fisher_mat, "steps_log": steps,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Fisher information value or matrix.
        """
        return f"I = {sd['fisher']}"


@register
class NaturalGradientGenerator(StepGenerator):
    """Compute one natural gradient descent step.

    Updates theta_{t+1} = theta_t - alpha * F^{-1} * grad L,
    where F is the Fisher information matrix (2x2) and grad is
    the Euclidean gradient.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "natural_gradient"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "natural gradient descent step"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a natural gradient step problem.

        Args:
            difficulty: Controls entry magnitude.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mag = min(1 + difficulty, 5)
        alpha = round(self._rng.choice([0.01, 0.05, 0.1, 0.5]), 4)

        # Fisher matrix (2x2 SPD): F = B^T B + I
        b11 = self._rng.randint(1, mag)
        b12 = self._rng.randint(-mag, mag)
        b22 = self._rng.randint(1, mag)
        F = [[b11 * b11 + b12 * b12 + 1, b11 * 0 + b12 * b22],
             [b11 * 0 + b12 * b22, b22 * b22 + 1]]

        # Gradient
        grad = [round(self._rng.uniform(-mag, mag), 4),
                round(self._rng.uniform(-mag, mag), 4)]

        # Theta
        theta = [round(self._rng.uniform(-2.0, 2.0), 4),
                 round(self._rng.uniform(-2.0, 2.0), 4)]

        # Invert 2x2 Fisher
        det = F[0][0] * F[1][1] - F[0][1] * F[1][0]
        if abs(det) < 1e-10:
            F[0][0] += 2
            F[1][1] += 2
            det = F[0][0] * F[1][1] - F[0][1] * F[1][0]

        Finv = [[round(F[1][1] / det, 4), round(-F[0][1] / det, 4)],
                [round(-F[1][0] / det, 4), round(F[0][0] / det, 4)]]

        # Natural gradient: F^{-1} * grad
        nat_grad = [round(Finv[i][0] * grad[0] + Finv[i][1] * grad[1], 4)
                    for i in range(2)]

        # Update
        theta_new = [round(theta[i] - alpha * nat_grad[i], 4)
                     for i in range(2)]

        steps_log = [
            f"F = {F}, det(F) = {round(det, 4)}",
            f"F^-1 = {Finv}",
            f"grad = {grad}",
            f"nat_grad = F^-1 * grad = {nat_grad}",
            f"theta_new = theta - alpha*nat_grad = {theta_new}",
        ]

        problem = (
            f"Natural gradient: theta={theta}, alpha={alpha}, "
            f"F={F}, grad={grad}"
        )
        return problem, {
            "theta_new": theta_new, "nat_grad": nat_grad,
            "steps_log": steps_log,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Updated parameter vector.
        """
        return f"theta_new = {sd['theta_new']}"


@register
class KLGeometryGenerator(StepGenerator):
    """Compute KL divergence between two normal distributions.

    KL(p||q) = (mu1-mu2)^2/(2*sigma2^2) + sigma1^2/(2*sigma2^2)
               - 1/2 + log(sigma2/sigma1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kl_geometry"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "KL divergence between two normals"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a KL divergence problem for two normals.

        Args:
            difficulty: Controls parameter range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mag = min(1 + difficulty, 5)
        mu1 = round(self._rng.uniform(-mag, mag), 4)
        mu2 = round(self._rng.uniform(-mag, mag), 4)
        sigma1 = round(self._rng.uniform(0.3, mag), 4)
        sigma2 = round(self._rng.uniform(0.3, mag), 4)

        s2_sq = sigma2 * sigma2
        term1 = (mu1 - mu2) ** 2 / (2 * s2_sq)
        term2 = (sigma1 * sigma1) / (2 * s2_sq)
        term3 = -0.5
        term4 = math.log(sigma2 / sigma1)
        kl = term1 + term2 + term3 + term4

        steps_log = [
            f"p = N({mu1}, {sigma1}^2), q = N({mu2}, {sigma2}^2)",
            f"(mu1-mu2)^2/(2*sig2^2) = {round(term1, 4)}",
            f"sig1^2/(2*sig2^2) = {round(term2, 4)}",
            f"log(sig2/sig1) = {round(term4, 4)}",
            f"KL = {round(term1, 4)} + {round(term2, 4)} - 0.5 + {round(term4, 4)}",
        ]

        problem = (
            f"KL(N({mu1},{sigma1}^2) || N({mu2},{sigma2}^2))"
        )
        return problem, {"kl": round(kl, 4), "steps_log": steps_log}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            KL divergence value.
        """
        return f"KL = {sd['kl']}"


@register
class ExponentialFamilyGenerator(StepGenerator):
    """Write a distribution in exponential family form.

    Identifies the natural parameter eta(theta), sufficient statistic
    T(x), log-partition A(theta), and base measure h(x) for
    Bernoulli, Poisson, and Normal distributions.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "exponential_family"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "exponential family canonical form"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an exponential family identification problem.

        Args:
            difficulty: Controls which distribution is selected.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        families = ["bernoulli", "poisson", "normal"]
        if difficulty <= 3:
            family = "bernoulli"
        elif difficulty <= 5:
            family = self._rng.choice(["bernoulli", "poisson"])
        else:
            family = self._rng.choice(families)

        if family == "bernoulli":
            p = round(self._rng.uniform(0.15, 0.85), 4)
            eta = round(math.log(p / (1 - p)), 4)
            steps = [
                f"Bernoulli(p={p}): f(x|p) = p^x * (1-p)^(1-x)",
                f"= exp(x*log(p/(1-p)) + log(1-p))",
                f"eta = log(p/(1-p)) = {eta}",
                f"T(x) = x, h(x) = 1",
                f"A(eta) = log(1 + exp(eta)) = {round(math.log(1 + math.exp(eta)), 4)}",
            ]
            problem = f"Exponential form of Bernoulli(p={p})"
            return problem, {
                "family": family, "eta": eta,
                "T": "x", "h": "1",
                "A": round(math.log(1 + math.exp(eta)), 4),
                "steps_log": steps,
            }
        elif family == "poisson":
            lam = round(self._rng.uniform(0.5, 8.0), 4)
            eta = round(math.log(lam), 4)
            A_val = round(lam, 4)
            steps = [
                f"Poisson(lam={lam}): f(x|lam) = lam^x * exp(-lam) / x!",
                f"= exp(x*log(lam) - lam) / x!",
                f"eta = log(lam) = {eta}",
                f"T(x) = x, h(x) = 1/x!",
                f"A(eta) = exp(eta) = lam = {A_val}",
            ]
            problem = f"Exponential form of Poisson(lam={lam})"
            return problem, {
                "family": family, "eta": eta,
                "T": "x", "h": "1/x!",
                "A": A_val, "steps_log": steps,
            }
        else:
            mu = round(self._rng.uniform(-5.0, 5.0), 4)
            sigma = round(self._rng.uniform(0.5, 3.0), 4)
            s2 = sigma * sigma
            eta1 = round(mu / s2, 4)
            eta2 = round(-1.0 / (2 * s2), 4)
            A_val = round(mu * mu / (2 * s2) + math.log(sigma * math.sqrt(2 * math.pi)), 4)
            steps = [
                f"Normal(mu={mu}, sigma={sigma})",
                f"eta = (mu/sigma^2, -1/(2*sigma^2)) = ({eta1}, {eta2})",
                f"T(x) = (x, x^2)",
                f"h(x) = 1",
                f"A(eta) = {A_val}",
            ]
            problem = f"Exponential form of Normal(mu={mu}, sigma={sigma})"
            return problem, {
                "family": family,
                "eta": [eta1, eta2],
                "T": "(x, x^2)", "h": "1",
                "A": A_val, "steps_log": steps,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        """Extract the final answer.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            Natural parameter, sufficient statistic, and log-partition.
        """
        return f"eta={sd['eta']}, T={sd['T']}, A={sd['A']}"
