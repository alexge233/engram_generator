"""Knowledge atoms for real analysis and probability distributions.

Registers theorem and formula atoms covering convergence tests,
sequences, series, and probability distributions. Each atom stores
the full authoritative statement sourced from Wikipedia, a worked
example, tier, domain, source citation, source URL, and prerequisites.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Real Analysis (tier 5-6)
# =========================================================================

register_atom(Atom(
    atom_type="definition",
    name="epsilon_delta",
    content=(
        "The epsilon-delta definition of a limit states that the limit "
        "of f(x) as x approaches c equals L if for every epsilon > 0 "
        "there exists a delta > 0 such that for all x, 0 < |x - c| < delta "
        "implies |f(x) - L| < epsilon. This is the rigorous foundation "
        "of calculus, replacing intuitive notions of 'approaching' with "
        "precise quantifier-based conditions."
    ),
    example=(
        "Prove lim(x->2) 3x+1 = 7: Given epsilon > 0, choose delta = epsilon/3. "
        "If 0 < |x-2| < delta, then |3x+1-7| = |3x-6| = 3|x-2| < 3*epsilon/3 = epsilon."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Limit of a function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/(%CE%B5,_%CE%B4)-definition_of_limit",
    prerequisites=["sequence_convergence"],
))

register_atom(Atom(
    atom_type="definition",
    name="cauchy_sequence",
    content=(
        "A Cauchy sequence is a sequence (a_n) such that for every "
        "epsilon > 0 there exists N such that for all m, n > N, "
        "|a_m - a_n| < epsilon. In the real numbers, a sequence converges "
        "if and only if it is Cauchy (completeness of R). This criterion "
        "allows proving convergence without knowing the limit."
    ),
    example=(
        "a_n = 1/n is Cauchy: |1/m - 1/n| <= 1/m + 1/n < 2/N for m,n > N. "
        "Choose N > 2/epsilon. The sequence converges to 0."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Cauchy sequence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cauchy_sequence",
    prerequisites=["sequence_convergence"],
))

register_atom(Atom(
    atom_type="definition",
    name="sequence_convergence",
    content=(
        "A sequence (a_n) converges to a limit L if for every epsilon > 0 "
        "there exists N such that for all n > N, |a_n - L| < epsilon. "
        "This is written lim(n->inf) a_n = L or a_n -> L. A sequence "
        "that does not converge is said to diverge."
    ),
    example=(
        "a_n = (2n+1)/(n+3): lim = lim (2+1/n)/(1+3/n) = 2/1 = 2. "
        "For n=100: a_100 = 201/103 = 1.9515, close to 2."
    ),
    tier=5,
    domain="real_analysis",
    source="Wikipedia contributors, 'Limit of a sequence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Limit_of_a_sequence",
    prerequisites=["addition", "division"],
))

register_atom(Atom(
    atom_type="definition",
    name="supremum_infimum",
    content=(
        "The supremum (least upper bound) of a set S is the smallest "
        "real number that is greater than or equal to every element of S. "
        "The infimum (greatest lower bound) is the largest real number "
        "that is less than or equal to every element of S. The "
        "completeness axiom of the reals guarantees that every "
        "non-empty bounded-above subset of R has a supremum in R."
    ),
    example=(
        "S = {1/n : n in N} = {1, 1/2, 1/3, ...}. "
        "sup(S) = 1 (attained at n=1). inf(S) = 0 (not attained, but "
        "every neighbourhood of 0 contains elements of S)."
    ),
    tier=5,
    domain="real_analysis",
    source="Wikipedia contributors, 'Infimum and supremum', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Infimum_and_supremum",
    prerequisites=["sequence_convergence"],
))

register_atom(Atom(
    atom_type="definition",
    name="uniform_convergence",
    content=(
        "A sequence of functions f_n converges uniformly to f on a set S "
        "if for every epsilon > 0 there exists N such that for all n > N "
        "and for all x in S, |f_n(x) - f(x)| < epsilon. Unlike pointwise "
        "convergence, N does not depend on x. Uniform convergence "
        "preserves continuity: if each f_n is continuous and f_n -> f "
        "uniformly, then f is continuous."
    ),
    example=(
        "f_n(x) = x^n on [0,1): converges pointwise to 0, but not uniformly "
        "since sup|f_n(x)| = sup x^n -> 1 as x->1. On [0, 1/2]: "
        "sup|f_n(x)| = (1/2)^n -> 0, so convergence is uniform on [0,1/2]."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Uniform convergence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Uniform_convergence",
    prerequisites=["sequence_convergence", "epsilon_delta"],
))

register_atom(Atom(
    atom_type="theorem",
    name="pointwise_vs_uniform",
    content=(
        "Pointwise convergence: f_n -> f pointwise on S if for each x in S, "
        "lim f_n(x) = f(x). Uniform convergence: f_n -> f uniformly if "
        "sup_x |f_n(x) - f(x)| -> 0. Uniform implies pointwise but not "
        "conversely. The Weierstrass M-test provides a sufficient condition: "
        "if |f_n(x)| <= M_n for all x and sum M_n converges, then sum f_n "
        "converges uniformly and absolutely."
    ),
    example=(
        "f_n(x) = x/n on [0,1]: f_n -> 0 pointwise. sup|x/n| = 1/n -> 0, "
        "so convergence is uniform. But g_n(x) = x^n on [0,1]: g_n -> 0 "
        "pointwise on [0,1) but sup|x^n| = 1 for all n, not uniform."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Pointwise convergence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pointwise_convergence",
    prerequisites=["uniform_convergence"],
))

register_atom(Atom(
    atom_type="theorem",
    name="ratio_test",
    content=(
        "The ratio test for convergence of an infinite series sum a_n: "
        "compute L = lim |a_{n+1}/a_n|. If L < 1, the series converges "
        "absolutely. If L > 1 or L = infinity, the series diverges. "
        "If L = 1, the test is inconclusive. The test is most useful "
        "for series involving factorials and exponentials."
    ),
    example=(
        "sum n!/n^n: L = lim ((n+1)!/(n+1)^{n+1}) / (n!/n^n) "
        "= lim (n/(n+1))^n = 1/e < 1. Series converges."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Ratio test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ratio_test",
    prerequisites=["sequence_convergence"],
))

register_atom(Atom(
    atom_type="theorem",
    name="root_test",
    content=(
        "The root test (Cauchy's root test) for convergence of sum a_n: "
        "compute L = lim sup |a_n|^{1/n}. If L < 1, the series converges "
        "absolutely. If L > 1, the series diverges. If L = 1, the test "
        "is inconclusive. The root test is stronger than the ratio test: "
        "whenever the ratio test gives a result, the root test gives "
        "the same result, but the root test may succeed when the ratio "
        "test fails."
    ),
    example=(
        "sum (2/3)^n: L = lim |(2/3)^n|^{1/n} = 2/3 < 1. "
        "Series converges. Sum = 1/(1-2/3) = 3 (geometric series)."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Root test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Root_test",
    prerequisites=["sequence_convergence"],
))

register_atom(Atom(
    atom_type="theorem",
    name="comparison_test",
    content=(
        "The comparison test: if 0 <= a_n <= b_n for all sufficiently "
        "large n, then: (1) if sum b_n converges, then sum a_n converges; "
        "(2) if sum a_n diverges, then sum b_n diverges. The limit "
        "comparison test: if lim a_n/b_n = c where 0 < c < infinity, "
        "then sum a_n and sum b_n either both converge or both diverge."
    ),
    example=(
        "Does sum 1/(n^2+1) converge? Compare: 1/(n^2+1) < 1/n^2, "
        "and sum 1/n^2 = pi^2/6 converges (p-series, p=2>1). "
        "By comparison test, sum 1/(n^2+1) converges."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Comparison test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Comparison_test",
    prerequisites=["sequence_convergence"],
))

register_atom(Atom(
    atom_type="theorem",
    name="alternating_series",
    content=(
        "The alternating series test (Leibniz test): if (a_n) is a "
        "monotonically decreasing sequence of positive terms with "
        "lim a_n = 0, then the alternating series sum (-1)^n a_n "
        "converges. Moreover, the partial sum S_n satisfies "
        "|S - S_n| <= a_{n+1} (the error is bounded by the first "
        "omitted term)."
    ),
    example=(
        "sum (-1)^{n+1}/n = 1 - 1/2 + 1/3 - 1/4 + ... = ln(2). "
        "a_n = 1/n is decreasing and lim 1/n = 0, so the series "
        "converges. After 4 terms: S_4 = 0.5833, |ln(2)-S_4| = 0.1098 < 1/5 = 0.2."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Alternating series test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Alternating_series_test",
    prerequisites=["sequence_convergence"],
))

register_atom(Atom(
    atom_type="theorem",
    name="power_series_radius",
    content=(
        "The radius of convergence R of a power series sum a_n x^n is "
        "given by R = 1/lim sup |a_n|^{1/n} (Cauchy-Hadamard formula), "
        "or equivalently R = lim |a_n/a_{n+1}| when this limit exists. "
        "The series converges absolutely for |x| < R and diverges for "
        "|x| > R. Convergence at |x| = R must be checked separately."
    ),
    example=(
        "sum x^n/n!: R = lim |n!/(n+1)!| = lim 1/(n+1) = infinity. "
        "The series converges for all x (it equals e^x)."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Radius of convergence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Radius_of_convergence",
    prerequisites=["ratio_test", "root_test"],
))

register_atom(Atom(
    atom_type="theorem",
    name="intermediate_value",
    content=(
        "The intermediate value theorem: if f is continuous on [a,b] "
        "and d is any value between f(a) and f(b), then there exists "
        "c in (a,b) such that f(c) = d. A corollary: if f is continuous "
        "on [a,b] and f(a) and f(b) have opposite signs, then f has "
        "a zero in (a,b). This theorem requires the completeness of "
        "the real numbers and does not hold over the rationals."
    ),
    example=(
        "f(x) = x^3 - x - 1 on [1,2]: f(1) = -1 < 0, f(2) = 5 > 0. "
        "By IVT, there exists c in (1,2) with f(c) = 0. "
        "Bisection: f(1.5) = 0.875 > 0, so c in (1, 1.5). The root is c = 1.3247..."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Intermediate value theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Intermediate_value_theorem",
    prerequisites=["epsilon_delta"],
))


# =========================================================================
# Probability Distributions (tier 4-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="negative_binomial",
    content=(
        "The negative binomial distribution models the number of "
        "failures before the r-th success in independent Bernoulli "
        "trials with success probability p. The PMF is: "
        "P(X=k) = C(k+r-1, k) * p^r * (1-p)^k for k = 0, 1, 2, ... "
        "Mean = r(1-p)/p, Variance = r(1-p)/p^2."
    ),
    example=(
        "r=3, p=0.5, k=2: P(X=2) = C(4,2) * 0.5^3 * 0.5^2 "
        "= 6 * 0.125 * 0.25 = 0.1875."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Negative binomial distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Negative_binomial_distribution",
    prerequisites=["binomial_dist"],
))

register_atom(Atom(
    atom_type="formula",
    name="hypergeometric",
    content=(
        "The hypergeometric distribution models draws without replacement. "
        "Given a population of N items with K successes, the probability "
        "of k successes in n draws is: "
        "P(X=k) = C(K,k)*C(N-K,n-k)/C(N,n). "
        "Mean = nK/N, Variance = n*K*(N-K)*(N-n)/(N^2*(N-1))."
    ),
    example=(
        "N=52, K=13 (hearts), n=5, k=2: P(X=2) = C(13,2)*C(39,3)/C(52,5) "
        "= 78*9139/2598960 = 712642/2598960 = 0.2743."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Hypergeometric distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hypergeometric_distribution",
    prerequisites=["binomial_dist", "counting"],
))

register_atom(Atom(
    atom_type="formula",
    name="geometric_dist",
    content=(
        "The geometric distribution models the number of trials needed "
        "to get the first success in independent Bernoulli trials with "
        "success probability p. P(X=k) = (1-p)^{k-1} * p for k = 1, 2, ... "
        "Mean = 1/p, Variance = (1-p)/p^2. The distribution is memoryless: "
        "P(X > m+n | X > m) = P(X > n)."
    ),
    example=(
        "p=1/6 (rolling a 6): P(X=3) = (5/6)^2 * (1/6) "
        "= 25/216 = 0.1157. Mean = 6 trials to first six."
    ),
    tier=4,
    domain="probability",
    source="Wikipedia contributors, 'Geometric distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Geometric_distribution",
    prerequisites=["basic_prob"],
))

register_atom(Atom(
    atom_type="formula",
    name="uniform_continuous",
    content=(
        "The continuous uniform distribution on [a,b] has constant "
        "probability density f(x) = 1/(b-a) for a <= x <= b, and 0 "
        "otherwise. CDF: F(x) = (x-a)/(b-a). "
        "Mean = (a+b)/2, Variance = (b-a)^2/12."
    ),
    example=(
        "U[2,8]: f(x) = 1/6, Mean = 5, Var = 36/12 = 3. "
        "P(3 < X < 5) = (5-3)/(8-2) = 2/6 = 1/3."
    ),
    tier=4,
    domain="probability",
    source="Wikipedia contributors, 'Continuous uniform distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Continuous_uniform_distribution",
    prerequisites=["basic_prob"],
))

register_atom(Atom(
    atom_type="formula",
    name="exponential_dist",
    content=(
        "The exponential distribution models time between events in a "
        "Poisson process with rate lambda. PDF: f(x) = lambda*exp(-lambda*x) "
        "for x >= 0. CDF: F(x) = 1 - exp(-lambda*x). "
        "Mean = 1/lambda, Variance = 1/lambda^2. "
        "The distribution is memoryless: P(X > s+t | X > s) = P(X > t)."
    ),
    example=(
        "lambda=0.5 (mean time = 2): P(X > 3) = exp(-0.5*3) "
        "= exp(-1.5) = 0.2231. P(1 < X < 4) = exp(-0.5) - exp(-2) = 0.4712."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Exponential distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exponential_distribution",
    prerequisites=["basic_prob"],
))

register_atom(Atom(
    atom_type="formula",
    name="normal_dist_compute",
    content=(
        "The normal (Gaussian) distribution with mean mu and standard "
        "deviation sigma has PDF: f(x) = (1/(sigma*sqrt(2*pi))) * "
        "exp(-(x-mu)^2/(2*sigma^2)). The standard normal Z = (X-mu)/sigma "
        "has mean 0 and variance 1. By the 68-95-99.7 rule, approximately "
        "68% of values fall within 1 sigma, 95% within 2, 99.7% within 3."
    ),
    example=(
        "mu=100, sigma=15: P(X < 115) = P(Z < 1) = 0.8413. "
        "P(85 < X < 115) = P(-1 < Z < 1) = 0.6827."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Normal distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Normal_distribution",
    prerequisites=["expected_value", "variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="joint_probability",
    content=(
        "The joint probability distribution of two random variables X and Y "
        "gives P(X=x, Y=y) for discrete variables or a joint density "
        "f(x,y) for continuous variables. Marginal distributions are "
        "obtained by summing/integrating: P(X=x) = sum_y P(X=x, Y=y). "
        "X and Y are independent iff P(X=x, Y=y) = P(X=x)*P(Y=y) for all x,y."
    ),
    example=(
        "Joint PMF: P(X=0,Y=0)=0.1, P(X=0,Y=1)=0.2, P(X=1,Y=0)=0.3, "
        "P(X=1,Y=1)=0.4. Marginal: P(X=0) = 0.1+0.2 = 0.3, "
        "P(X=1) = 0.3+0.4 = 0.7."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Joint probability distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Joint_probability_distribution",
    prerequisites=["basic_prob", "conditional_prob"],
))

register_atom(Atom(
    atom_type="formula",
    name="covariance_correlation",
    content=(
        "The covariance of X and Y is Cov(X,Y) = E[(X-E[X])(Y-E[Y])] "
        "= E[XY] - E[X]*E[Y]. The Pearson correlation coefficient is "
        "rho = Cov(X,Y)/(sigma_X * sigma_Y), bounded in [-1, 1]. "
        "rho = 0 implies no linear relationship; rho = +/-1 implies "
        "perfect linear relationship."
    ),
    example=(
        "X = {1,2,3}, Y = {2,4,5}: E[X]=2, E[Y]=3.667, E[XY]=8.333, "
        "Cov = 8.333 - 2*3.667 = 1.0, sigma_X=0.8165, sigma_Y=1.247, "
        "rho = 1.0/(0.8165*1.247) = 0.9820."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Covariance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Covariance",
    prerequisites=["expected_value", "variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="order_statistics",
    content=(
        "The k-th order statistic X_(k) of a sample of size n is the "
        "k-th smallest value. X_(1) is the minimum, X_(n) is the maximum. "
        "For a continuous distribution with CDF F and PDF f, the PDF of "
        "X_(k) is: f_{X_(k)}(x) = n!/(k-1)!(n-k)! * F(x)^{k-1} * "
        "(1-F(x))^{n-k} * f(x)."
    ),
    example=(
        "Sample {3,1,4,1,5}: sorted = {1,1,3,4,5}. "
        "X_(1)=1 (min), X_(3)=3 (median), X_(5)=5 (max). "
        "Range = X_(5)-X_(1) = 4."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Order statistic', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Order_statistic",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="formula",
    name="gamma_dist",
    content=(
        "The gamma distribution with shape alpha > 0 and rate beta > 0 "
        "has PDF: f(x) = beta^alpha * x^{alpha-1} * exp(-beta*x) / Gamma(alpha) "
        "for x > 0. Mean = alpha/beta, Variance = alpha/beta^2. "
        "Special cases: alpha=1 gives the exponential distribution; "
        "alpha=n/2, beta=1/2 gives the chi-squared distribution with n d.f."
    ),
    example=(
        "alpha=3, beta=2: Mean = 3/2 = 1.5, Var = 3/4 = 0.75. "
        "Mode = (alpha-1)/beta = 2/2 = 1.0."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Gamma distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gamma_distribution",
    prerequisites=["exponential_dist"],
))

register_atom(Atom(
    atom_type="formula",
    name="multivariate_normal",
    content=(
        "The multivariate normal distribution in d dimensions with mean "
        "vector mu and covariance matrix Sigma has PDF: "
        "f(x) = (2*pi)^{-d/2} |Sigma|^{-1/2} exp(-0.5*(x-mu)^T Sigma^{-1} (x-mu)). "
        "Marginal distributions are normal; conditional distributions are also "
        "normal with formulas mu_{a|b} = mu_a + Sigma_{ab}*Sigma_{bb}^{-1}*(x_b - mu_b)."
    ),
    example=(
        "d=2, mu=[0,0], Sigma=[[1,0.5],[0.5,1]]: |Sigma| = 0.75, "
        "f(0,0) = (2*pi)^{-1} * 0.75^{-0.5} = 0.1837."
    ),
    tier=6,
    domain="probability",
    source="Wikipedia contributors, 'Multivariate normal distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Multivariate_normal_distribution",
    prerequisites=["normal_dist_compute", "matrix_inverse"],
))

register_atom(Atom(
    atom_type="formula",
    name="transformation_rv",
    content=(
        "If X is a continuous random variable with PDF f_X and Y = g(X) "
        "where g is monotone and differentiable, then the PDF of Y is: "
        "f_Y(y) = f_X(g^{-1}(y)) * |d/dy g^{-1}(y)|. "
        "For the general case (non-monotone g), the formula sums over "
        "all branches of the inverse."
    ),
    example=(
        "X ~ U[0,1], Y = -ln(X): g^{-1}(y) = e^{-y}, "
        "|d/dy e^{-y}| = e^{-y}. f_Y(y) = 1 * e^{-y} = e^{-y} for y>0. "
        "So Y ~ Exp(1)."
    ),
    tier=5,
    domain="probability",
    source="Wikipedia contributors, 'Probability density function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Probability_density_function#Function_of_random_variables_and_change_of_variables_in_the_probability_density_function",
    prerequisites=["exponential_dist", "chain_rule"],
))
