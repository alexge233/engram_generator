"""Knowledge atoms for queuing theory, Bayesian statistics, and causal inference."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Queuing theory (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="erlang_b",
    content=(
        "The Erlang B formula gives the blocking probability in a loss "
        "system with c servers and offered load A (in Erlangs): "
        "B(c, A) = (A^c / c!) / sum_{k=0}^{c} (A^k / k!). "
        "It assumes Poisson arrivals and exponential service times with "
        "no waiting room (blocked calls are lost)."
    ),
    example=(
        "Given A = 2 Erlangs, c = 3 servers: "
        "numerator = 2^3/3! = 8/6 = 1.333. "
        "denominator = 1 + 2 + 2 + 1.333 = 6.333. "
        "B(3,2) = 1.333/6.333 = 0.2105."
    ),
    tier=5,
    domain="queuing_theory",
    source="Wikipedia contributors, 'Erlang B formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Erlang_B_formula",
    prerequisites=["factorial"],
))

register_atom(Atom(
    atom_type="formula",
    name="erlang_c",
    content=(
        "The Erlang C formula gives the probability that an arriving "
        "customer must wait in queue in an M/M/c system: "
        "C(c, A) = [A^c/c! * c/(c-A)] / [sum_{k=0}^{c-1}(A^k/k!) + A^c/c! * c/(c-A)]. "
        "A is the offered load in Erlangs and c is the number of servers."
    ),
    example=(
        "Given A = 1.5 Erlangs, c = 2: "
        "A^c/c! = 1.5^2/2 = 1.125. c/(c-A) = 2/0.5 = 4. "
        "Numerator = 1.125*4 = 4.5. Denominator = 1+1.5+4.5 = 7. "
        "C(2,1.5) = 4.5/7 = 0.6429."
    ),
    tier=5,
    domain="queuing_theory",
    source="Wikipedia contributors, 'Erlang C formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Erlang_C_formula",
    prerequisites=["erlang_b"],
))

register_atom(Atom(
    atom_type="law",
    name="littles_law",
    content=(
        "Little's law relates the long-term average number of customers "
        "L in a stationary system to the long-term average arrival rate "
        "lambda and the average time W a customer spends in the system: "
        "L = lambda * W. The law is remarkably general and applies to "
        "any stable queueing system regardless of arrival or service "
        "distributions."
    ),
    example=(
        "If customers arrive at rate lambda = 10/hr and each spends "
        "W = 0.5 hr in the system: L = 10 * 0.5 = 5 customers "
        "on average in the system."
    ),
    tier=5,
    domain="queuing_theory",
    source="Wikipedia contributors, 'Little's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Little%27s_law",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="mg1_queue",
    content=(
        "The M/G/1 queue has Poisson arrivals (rate lambda) and a single "
        "server with general service time distribution (mean E[S], second "
        "moment E[S^2]). The Pollaczek-Khinchine formula gives mean queue "
        "length: Lq = lambda^2 * E[S^2] / (2*(1 - rho)), where "
        "rho = lambda * E[S] is the server utilisation."
    ),
    example=(
        "lambda = 4/hr, E[S] = 0.2 hr, E[S^2] = 0.05 hr^2: "
        "rho = 4*0.2 = 0.8. Lq = 16*0.05 / (2*0.2) = 0.8/0.4 = 2."
    ),
    tier=6,
    domain="queuing_theory",
    source="Wikipedia contributors, 'M/G/1 queue', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/M/G/1_queue",
    prerequisites=["mm1_queue"],
))

register_atom(Atom(
    atom_type="concept",
    name="jackson_network",
    content=(
        "A Jackson network is an open network of queues where each node "
        "is an M/M/c_i queue, external arrivals are Poisson, routing is "
        "Markovian, and service times are exponential. Jackson's theorem "
        "states that the stationary distribution is the product of the "
        "marginal distributions of each node, so nodes behave as if "
        "independent."
    ),
    example=(
        "Two-node network: external arrival rate gamma_1 = 5, "
        "gamma_2 = 0. Routing p_12 = 0.3, p_21 = 0. "
        "Effective rates: lambda_1 = 5, lambda_2 = 5*0.3 = 1.5. "
        "Each node analysed independently as M/M/1."
    ),
    tier=6,
    domain="queuing_theory",
    source="Wikipedia contributors, 'Jackson network', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Jackson_network",
    prerequisites=["mm1_queue"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="priority_queue",
    content=(
        "A priority queue with preemptive or non-preemptive service "
        "disciplines serves higher-priority customers first. In an "
        "M/M/1 priority queue with K classes, the mean waiting time "
        "for class k depends on the total load from higher-priority "
        "classes: W_k = W_0 / ((1 - sigma_{k-1})(1 - sigma_k)), "
        "where sigma_k = sum_{i=1}^{k} rho_i."
    ),
    example=(
        "Two classes: rho_1 = 0.3, rho_2 = 0.4, mu = 1. "
        "W_0 = rho/(mu(1-rho)) base wait. "
        "W_1 = W_0 / (1*(1-0.3)) = W_0/0.7. "
        "W_2 = W_0 / ((1-0.3)(1-0.7)) = W_0/0.21."
    ),
    tier=6,
    domain="queuing_theory",
    source="Wikipedia contributors, 'Priority queue (queueing theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Priority_queue_(queueing_theory)",
    prerequisites=["mm1_queue"],
))

# ---------------------------------------------------------------------------
# Bayesian statistics (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="concept",
    name="conjugate_prior",
    content=(
        "A conjugate prior is a prior distribution that, when combined "
        "with the likelihood function via Bayes' theorem, yields a "
        "posterior distribution in the same family as the prior. For "
        "example, a Beta(alpha, beta) prior is conjugate to the "
        "Binomial likelihood, giving posterior Beta(alpha+k, beta+n-k)."
    ),
    example=(
        "Prior: Beta(2, 5). Data: 3 successes in 10 trials. "
        "Posterior: Beta(2+3, 5+7) = Beta(5, 12). "
        "Posterior mean = 5/17 = 0.2941."
    ),
    tier=5,
    domain="bayesian_statistics",
    source="Wikipedia contributors, 'Conjugate prior', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conjugate_prior",
    prerequisites=["bayes_theorem"],
))

register_atom(Atom(
    atom_type="concept",
    name="posterior_predictive",
    content=(
        "The posterior predictive distribution integrates out the "
        "parameter uncertainty: p(x_new | data) = integral p(x_new | theta) "
        "p(theta | data) d_theta. For a Beta-Binomial model with "
        "posterior Beta(a, b), the predictive probability of success is "
        "simply a / (a + b), the posterior mean."
    ),
    example=(
        "Posterior: Beta(5, 12). P(next success) = 5/(5+12) = 0.2941. "
        "For n=10 future trials, predicted successes follow "
        "Beta-Binomial(10, 5, 12)."
    ),
    tier=6,
    domain="bayesian_statistics",
    source="Wikipedia contributors, 'Posterior predictive distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Posterior_predictive_distribution",
    prerequisites=["conjugate_prior"],
))

register_atom(Atom(
    atom_type="concept",
    name="credible_interval",
    content=(
        "A Bayesian credible interval [a, b] contains the parameter "
        "with probability P given the data: P(a <= theta <= b | data) = 1 - alpha. "
        "The highest posterior density (HPD) interval is the shortest "
        "such interval. Unlike frequentist confidence intervals, "
        "credible intervals have a direct probability interpretation."
    ),
    example=(
        "Posterior: Normal(mu=5.2, sigma=0.8). 95% credible interval: "
        "5.2 +/- 1.96*0.8 = [3.632, 6.768]."
    ),
    tier=5,
    domain="bayesian_statistics",
    source="Wikipedia contributors, 'Credible interval', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Credible_interval",
    prerequisites=["confidence_interval"],
))

register_atom(Atom(
    atom_type="concept",
    name="bayes_factor",
    content=(
        "The Bayes factor B_10 = P(data | M1) / P(data | M0) quantifies "
        "the evidence for model M1 over M0. B_10 > 10 is strong evidence "
        "for M1, 3-10 is moderate, 1-3 is weak, and < 1 favours M0. "
        "The marginal likelihood P(data | M) integrates the likelihood "
        "over the prior."
    ),
    example=(
        "M0: theta ~ Uniform(0,1), M1: theta = 0.5 (point). "
        "Data: 7 heads in 10 flips. P(data|M1) = C(10,7)*0.5^10 = 0.1172. "
        "P(data|M0) = 1/11 = 0.0909. B_10 = 0.1172/0.0909 = 1.29."
    ),
    tier=6,
    domain="bayesian_statistics",
    source="Wikipedia contributors, 'Bayes factor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bayes_factor",
    prerequisites=["bayes_theorem"],
))

register_atom(Atom(
    atom_type="concept",
    name="map_estimate",
    content=(
        "The maximum a posteriori (MAP) estimate is the mode of the "
        "posterior distribution: theta_MAP = argmax P(theta | data) = "
        "argmax P(data | theta) * P(theta). For a Beta(a,b) posterior, "
        "MAP = (a - 1) / (a + b - 2) when a, b > 1."
    ),
    example=(
        "Prior Beta(3, 5), data: 4 successes in 10 trials. "
        "Posterior Beta(7, 11). MAP = (7-1)/(7+11-2) = 6/16 = 0.375."
    ),
    tier=5,
    domain="bayesian_statistics",
    source="Wikipedia contributors, 'Maximum a posteriori estimation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Maximum_a_posteriori_estimation",
    prerequisites=["bayes_theorem"],
))

register_atom(Atom(
    atom_type="concept",
    name="empirical_bayes",
    content=(
        "Empirical Bayes methods estimate the prior distribution from "
        "the data itself, then use it for posterior inference. The "
        "James-Stein estimator shrinks individual estimates toward the "
        "grand mean: theta_EB_i = x_bar + (1 - (k-2)*sigma^2 / sum(x_i - x_bar)^2) "
        "* (x_i - x_bar)."
    ),
    example=(
        "5 group means: [3, 5, 7, 2, 8], grand mean = 5, sigma^2 = 1. "
        "Shrinkage factor B = (5-2)*1 / (4+0+4+9+9) = 3/26 = 0.115. "
        "theta_EB_1 = 5 + (1-0.115)*(3-5) = 5 - 1.77 = 3.23."
    ),
    tier=6,
    domain="bayesian_statistics",
    source="Wikipedia contributors, 'Empirical Bayes method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Empirical_Bayes_method",
    prerequisites=["map_estimate"],
))

# ---------------------------------------------------------------------------
# Causal inference (tier 5-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="concept",
    name="ate_compute",
    content=(
        "The Average Treatment Effect (ATE) is the expected causal "
        "effect of a treatment on an outcome across a population: "
        "ATE = E[Y(1)] - E[Y(0)], where Y(1) and Y(0) are potential "
        "outcomes under treatment and control. In a randomised trial, "
        "ATE = E[Y | T=1] - E[Y | T=0]."
    ),
    example=(
        "Treatment group mean Y = 78, control group mean Y = 72. "
        "ATE = 78 - 72 = 6. The treatment increases the outcome by "
        "6 units on average."
    ),
    tier=5,
    domain="causal_inference",
    source="Wikipedia contributors, 'Average treatment effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Average_treatment_effect",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="concept",
    name="propensity_score",
    content=(
        "The propensity score e(X) = P(T=1 | X) is the probability of "
        "receiving treatment given observed covariates X. Rosenbaum and "
        "Rubin (1983) showed that conditioning on the propensity score "
        "removes confounding bias: Y(t) is independent of T given e(X). "
        "Common methods: matching, stratification, inverse weighting."
    ),
    example=(
        "Logistic regression: logit(e) = -1 + 0.5*age + 0.3*income. "
        "For age=40, income=50K: logit(e) = -1 + 20 + 15 = 34. "
        "e = 1/(1+exp(-34)) ~ 1.0 (high propensity)."
    ),
    tier=6,
    domain="causal_inference",
    source="Wikipedia contributors, 'Propensity score matching', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Propensity_score_matching",
    prerequisites=["logistic_regression_compute"],
))

register_atom(Atom(
    atom_type="concept",
    name="instrumental_variable",
    content=(
        "An instrumental variable Z affects the treatment T but has no "
        "direct effect on the outcome Y (exclusion restriction) and is "
        "not confounded with Y. The IV estimator is: "
        "beta_IV = Cov(Y, Z) / Cov(T, Z). Two-stage least squares "
        "(2SLS) first regresses T on Z, then Y on predicted T."
    ),
    example=(
        "Z = distance to college, T = years of education, Y = wage. "
        "Cov(Y, Z) = -5, Cov(T, Z) = -0.5. "
        "beta_IV = -5 / -0.5 = 10 (each year of education "
        "increases wage by 10 units)."
    ),
    tier=6,
    domain="causal_inference",
    source="Wikipedia contributors, 'Instrumental variables estimation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Instrumental_variables_estimation",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="concept",
    name="diff_in_diff",
    content=(
        "Difference-in-differences (DiD) estimates a causal effect by "
        "comparing the change in outcomes over time between a treatment "
        "group and a control group: "
        "ATE = (Y_treat_post - Y_treat_pre) - (Y_ctrl_post - Y_ctrl_pre). "
        "The key assumption is parallel trends: absent treatment, both "
        "groups would have changed similarly."
    ),
    example=(
        "Treatment pre=50, post=70. Control pre=45, post=55. "
        "DiD = (70-50) - (55-45) = 20 - 10 = 10."
    ),
    tier=5,
    domain="causal_inference",
    source="Wikipedia contributors, 'Difference in differences', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Difference_in_differences",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="concept",
    name="regression_discontinuity",
    content=(
        "Regression discontinuity design (RDD) exploits a cutoff in an "
        "assignment variable to estimate causal effects. Units just above "
        "and below the cutoff are quasi-randomly assigned, so the jump "
        "in the outcome at the cutoff estimates the local average "
        "treatment effect (LATE)."
    ),
    example=(
        "Scholarship awarded if score >= 80. Comparing students at 79 vs 81: "
        "mean GPA at 81 = 3.4, at 79 = 3.1. LATE = 3.4 - 3.1 = 0.3."
    ),
    tier=6,
    domain="causal_inference",
    source="Wikipedia contributors, 'Regression discontinuity design', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Regression_discontinuity_design",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="concept",
    name="do_calculus",
    content=(
        "Pearl's do-calculus provides three rules for manipulating "
        "interventional distributions P(Y | do(X)) using a causal DAG: "
        "Rule 1 (insertion/deletion of observations), Rule 2 (exchange "
        "of interventions and observations), Rule 3 (insertion/deletion "
        "of interventions). A causal effect is identifiable if it can "
        "be reduced to observational quantities via these rules."
    ),
    example=(
        "DAG: Z -> X -> Y, Z -> Y. By backdoor adjustment: "
        "P(Y | do(X)) = sum_z P(Y | X, Z=z) P(Z=z). "
        "The confounding by Z is removed by conditioning."
    ),
    tier=7,
    domain="causal_inference",
    source="Wikipedia contributors, 'Do-calculus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Do-calculus",
    prerequisites=["bayes_theorem"],
))
