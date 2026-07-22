"""Knowledge atoms for optimization, astronomy, compilers, and stochastic calculus."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ---------------------------------------------------------------------------
# Optimization (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="linear_program",
    content=(
        "A linear program (LP) minimises or maximises a linear objective "
        "function subject to linear equality and inequality constraints. "
        "Standard form: minimise c^T x subject to Ax <= b, x >= 0. "
        "The feasible region is a convex polytope and the optimum, if "
        "finite, occurs at a vertex."
    ),
    example=(
        "Minimise z = -x1 - 2*x2 subject to x1 + x2 <= 4, x1 <= 3, "
        "x2 <= 3, x1,x2 >= 0. Optimal vertex: (1,3), z = -7."
    ),
    tier=5,
    domain="optimization",
    source="Wikipedia contributors, 'Linear programming', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Linear_programming",
    prerequisites=["system_equations"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="simplex_step",
    content=(
        "The simplex algorithm solves linear programs by moving along "
        "edges of the feasible polytope from vertex to vertex, each time "
        "improving the objective value. A pivot operation swaps a basic "
        "and non-basic variable. The entering variable has the most "
        "negative reduced cost; the leaving variable is determined by "
        "the minimum ratio test."
    ),
    example=(
        "Tableau: basis {s1,s2}, entering x2 (reduced cost -2), "
        "ratios 4/1=4 and 3/1=3, leaving s2. After pivot: x2=3, z=-6."
    ),
    tier=6,
    domain="optimization",
    source="Wikipedia contributors, 'Simplex algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Simplex_algorithm",
    prerequisites=["linear_program"],
))

register_atom(Atom(
    atom_type="theorem",
    name="dual_lp",
    content=(
        "Every linear program (the primal) has a dual linear program. "
        "If the primal is min c^T x s.t. Ax >= b, x >= 0, the dual is "
        "max b^T y s.t. A^T y <= c, y >= 0. Strong duality: if either "
        "has an optimal solution, so does the other and the optimal "
        "values are equal."
    ),
    example=(
        "Primal: min 3x1+5x2 s.t. x1>=1, x2>=1, x1+x2>=3. "
        "Dual: max y1+y2+3y3 s.t. y1+y3<=3, y2+y3<=5, y>=0. "
        "Both have optimal value 11."
    ),
    tier=6,
    domain="optimization",
    source="Wikipedia contributors, 'Dual linear program', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dual_linear_program",
    prerequisites=["linear_program"],
))

register_atom(Atom(
    atom_type="definition",
    name="convex_check",
    content=(
        "A function f: R^n -> R is convex if for all x, y and "
        "lambda in [0,1]: f(lambda*x + (1-lambda)*y) <= "
        "lambda*f(x) + (1-lambda)*f(y). For twice-differentiable "
        "functions, convexity is equivalent to the Hessian matrix "
        "being positive semidefinite everywhere."
    ),
    example=(
        "f(x,y) = x^2 + y^2. Hessian = [[2,0],[0,2]], eigenvalues "
        "2,2 > 0, so f is convex."
    ),
    tier=6,
    domain="optimization",
    source="Wikipedia contributors, 'Convex function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convex_function",
    prerequisites=["eigenvalue"],
))

register_atom(Atom(
    atom_type="theorem",
    name="kkt_conditions",
    content=(
        "The Karush-Kuhn-Tucker (KKT) conditions are first-order "
        "necessary conditions for a solution in nonlinear programming "
        "to be optimal, provided some regularity condition holds. "
        "They generalise Lagrange multipliers to inequality constraints: "
        "stationarity, primal feasibility, dual feasibility, and "
        "complementary slackness."
    ),
    example=(
        "Min x^2 + y^2 s.t. x + y >= 1. KKT: 2x - lambda = 0, "
        "2y - lambda = 0, lambda*(x+y-1) = 0, lambda >= 0. "
        "Solution: x=y=0.5, lambda=1."
    ),
    tier=6,
    domain="optimization",
    source="Wikipedia contributors, 'Karush-Kuhn-Tucker conditions', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Karush%E2%80%93Kuhn%E2%80%93Tucker_conditions",
    prerequisites=["gradient", "lagrange_multiplier"],
))

register_atom(Atom(
    atom_type="theorem",
    name="gradient_descent_convergence",
    content=(
        "Gradient descent updates x_{k+1} = x_k - alpha * grad f(x_k). "
        "For an L-smooth convex function with step size alpha = 1/L, "
        "the convergence rate is O(1/k): f(x_k) - f* <= L||x_0 - x*||^2 / (2k). "
        "For mu-strongly convex functions, linear convergence: "
        "||x_k - x*||^2 <= (1 - mu/L)^k ||x_0 - x*||^2."
    ),
    example=(
        "f(x) = x^2, L=2, mu=2, alpha=0.5. x0=4: "
        "x1 = 4 - 0.5*2*4 = 0. Converges in 1 step (quadratic, perfect)."
    ),
    tier=5,
    domain="optimization",
    source="Wikipedia contributors, 'Gradient descent', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gradient_descent",
    prerequisites=["gradient"],
))

# ---------------------------------------------------------------------------
# Astronomy (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="parallax_distance",
    content=(
        "Stellar parallax measures distance to nearby stars using "
        "the apparent shift in position as Earth orbits the Sun. "
        "d = 1/p, where d is distance in parsecs and p is the "
        "parallax angle in arcseconds. 1 parsec = 3.2616 light-years."
    ),
    example=(
        "Proxima Centauri: p = 0.7687 arcsec, d = 1/0.7687 = 1.301 pc "
        "= 4.244 light-years."
    ),
    tier=4,
    domain="astronomy",
    source="Wikipedia contributors, 'Stellar parallax', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stellar_parallax",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="definition",
    name="hr_diagram",
    content=(
        "The Hertzsprung-Russell (HR) diagram plots stellar luminosity "
        "against effective temperature (or spectral type). Stars cluster "
        "along the main sequence (hydrogen burning), with giants and "
        "supergiants above and white dwarfs below. A star's position "
        "indicates its evolutionary stage."
    ),
    example=(
        "Sun: T_eff = 5778 K, L = 1 L_sun, spectral type G2V, "
        "on the main sequence. Betelgeuse: T_eff ~ 3500 K, "
        "L ~ 100,000 L_sun, red supergiant."
    ),
    tier=4,
    domain="astronomy",
    source="Wikipedia contributors, 'Hertzsprung-Russell diagram', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hertzsprung%E2%80%93Russell_diagram",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="absolute_magnitude",
    content=(
        "Absolute magnitude M is the apparent magnitude m a star would "
        "have at a standard distance of 10 parsecs. The distance modulus "
        "relates them: m - M = 5 * log10(d/10), where d is in parsecs. "
        "Equivalently M = m - 5 * log10(d) + 5."
    ),
    example=(
        "Sirius: m = -1.46, d = 2.64 pc. M = -1.46 - 5*log10(2.64) + 5 "
        "= -1.46 - 2.11 + 5 = 1.43."
    ),
    tier=5,
    domain="astronomy",
    source="Wikipedia contributors, 'Absolute magnitude', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Absolute_magnitude",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="doppler_velocity",
    content=(
        "The Doppler effect for electromagnetic radiation relates the "
        "observed wavelength shift to the radial velocity of the source: "
        "v = c * (lambda_obs - lambda_emit) / lambda_emit = c * z, "
        "where z is the redshift. Valid for v << c (non-relativistic)."
    ),
    example=(
        "H-alpha rest wavelength 656.28 nm, observed at 656.92 nm: "
        "z = (656.92 - 656.28) / 656.28 = 0.000975, "
        "v = 3e5 * 0.000975 = 292.5 km/s (receding)."
    ),
    tier=5,
    domain="astronomy",
    source="Wikipedia contributors, 'Doppler effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Doppler_effect",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="tidal_force",
    content=(
        "Tidal force arises from the differential gravitational pull "
        "across an extended body. The tidal acceleration at distance r "
        "from a body of mass M is approximately dF/dr = -2GM/r^3 * dr, "
        "where dr is the size of the object. Tidal forces scale as "
        "M/r^3, so closer or more massive bodies produce stronger tides."
    ),
    example=(
        "Moon's tidal acceleration on Earth: M_moon = 7.342e22 kg, "
        "r = 3.844e8 m, dr = 6.371e6 m (Earth radius). "
        "a_tidal = 2*6.674e-11*7.342e22/(3.844e8)^3 * 6.371e6 "
        "= 1.10e-6 m/s^2."
    ),
    tier=5,
    domain="astronomy",
    source="Wikipedia contributors, 'Tidal force', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tidal_force",
    prerequisites=["gravitational_force"],
))

register_atom(Atom(
    atom_type="formula",
    name="drake_equation",
    content=(
        "The Drake equation estimates the number of active, "
        "communicative extraterrestrial civilisations in the Milky Way: "
        "N = R* * f_p * n_e * f_l * f_i * f_c * L, where R* is the "
        "rate of star formation, f_p is the fraction with planets, "
        "n_e is the number of habitable planets per system, f_l is the "
        "fraction developing life, f_i intelligence, f_c communication, "
        "and L is the lifespan of such civilisations."
    ),
    example=(
        "Drake's original: R*=1, f_p=0.5, n_e=2, f_l=1, f_i=0.01, "
        "f_c=0.01, L=10000. N = 1*0.5*2*1*0.01*0.01*10000 = 1."
    ),
    tier=4,
    domain="astronomy",
    source="Wikipedia contributors, 'Drake equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Drake_equation",
    prerequisites=["multiplication"],
))

# ---------------------------------------------------------------------------
# Compilers (tier 4-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="tokenize",
    content=(
        "Lexical analysis (tokenisation) is the first phase of a "
        "compiler. It reads a stream of characters and groups them into "
        "tokens (lexemes) such as identifiers, keywords, literals, and "
        "operators. Typically implemented as a finite automaton or "
        "using regular expressions."
    ),
    example=(
        "Input: 'int x = 42;'. Tokens: [KW:int, ID:x, OP:=, "
        "NUM:42, SEMI:;]."
    ),
    tier=4,
    domain="compilers",
    source="Wikipedia contributors, 'Lexical analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lexical_analysis",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="recursive_descent",
    content=(
        "Recursive descent parsing is a top-down parsing technique "
        "where each non-terminal in the grammar has a corresponding "
        "procedure. The parser starts with the start symbol and "
        "recursively expands non-terminals by matching against the "
        "input. Requires the grammar to be LL(1) or to use backtracking."
    ),
    example=(
        "Grammar: E -> T '+' E | T, T -> '(' E ')' | num. "
        "Input '3+4': parse_E() calls parse_T() which matches '3', "
        "then matches '+', then parse_E() matches '4'. Result: Add(3,4)."
    ),
    tier=5,
    domain="compilers",
    source="Wikipedia contributors, 'Recursive descent parser', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Recursive_descent_parser",
    prerequisites=["tokenize"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="first_follow_set",
    content=(
        "FIRST(A) is the set of terminals that can appear as the first "
        "symbol of any string derived from non-terminal A. FOLLOW(A) is "
        "the set of terminals that can appear immediately after A in "
        "some sentential form. Both are computed by fixed-point "
        "iteration and are used to build LL(1) parse tables."
    ),
    example=(
        "Grammar: S -> AB, A -> aA | e, B -> b. "
        "FIRST(A) = {a, e}, FIRST(B) = {b}, FIRST(S) = {a, b}. "
        "FOLLOW(A) = {b}, FOLLOW(B) = {$}, FOLLOW(S) = {$}."
    ),
    tier=5,
    domain="compilers",
    source="Wikipedia contributors, 'LL parser', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/LL_parser",
    prerequisites=["recursive_descent"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="ll1_parse_table",
    content=(
        "An LL(1) parse table is a 2D table indexed by non-terminal "
        "and lookahead terminal. Entry M[A, a] contains the production "
        "A -> alpha if a is in FIRST(alpha), or if alpha =>* e and a is "
        "in FOLLOW(A). If any cell has multiple entries, the grammar "
        "is not LL(1)."
    ),
    example=(
        "Grammar: S -> aS | b. FIRST(aS)={a}, FIRST(b)={b}. "
        "M[S,a] = S->aS, M[S,b] = S->b. No conflicts, grammar is LL(1)."
    ),
    tier=6,
    domain="compilers",
    source="Wikipedia contributors, 'LL parser', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/LL_parser#Constructing_an_LL(1)_parsing_table",
    prerequisites=["first_follow_set"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="type_check",
    content=(
        "Type checking verifies that a program's operations are applied "
        "to arguments of appropriate types. Static type checking is done "
        "at compile time using type inference rules. For example, in "
        "the simply-typed lambda calculus, the rule for application is: "
        "if e1: T1->T2 and e2: T1, then (e1 e2): T2."
    ),
    example=(
        "Expression: (lambda x:int. x + 1)(42). "
        "x:int, 1:int, (+):int->int->int, so x+1:int. "
        "lambda x:int. x+1 : int->int. 42:int. Application: int. Correct."
    ),
    tier=5,
    domain="compilers",
    source="Wikipedia contributors, 'Type system', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Type_system",
    prerequisites=["tokenize"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="lambda_reduce",
    content=(
        "Beta reduction is the fundamental computation rule of lambda "
        "calculus: (lambda x. M) N reduces to M[x := N], where all "
        "free occurrences of x in M are replaced by N (with renaming "
        "to avoid capture). A term is in normal form when no further "
        "beta reductions are possible."
    ),
    example=(
        "(lambda x. x) (lambda y. y) -> (lambda y. y). "
        "(lambda x. lambda y. x) a b -> (lambda y. a) b -> a."
    ),
    tier=6,
    domain="compilers",
    source="Wikipedia contributors, 'Lambda calculus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lambda_calculus#Beta_reduction",
    prerequisites=["recursive_descent"],
))

# ---------------------------------------------------------------------------
# Stochastic Calculus (tier 6-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="ito_lemma",
    content=(
        "Ito's lemma is the chain rule for stochastic calculus. If "
        "X_t satisfies dX = mu dt + sigma dW, and f(t,x) is twice "
        "differentiable, then df = (f_t + mu*f_x + 0.5*sigma^2*f_xx) dt "
        "+ sigma*f_x dW. The extra 0.5*sigma^2*f_xx term arises because "
        "(dW)^2 = dt."
    ),
    example=(
        "X_t = W_t (Brownian motion, mu=0, sigma=1), f(x) = x^2. "
        "f_x = 2x, f_xx = 2. df = (0 + 0 + 0.5*1*2) dt + 1*2x dW "
        "= dt + 2W_t dW. So W_t^2 = t + 2*integral(W_s dW_s)."
    ),
    tier=7,
    domain="stochastic_calculus",
    source="Wikipedia contributors, 'Ito's lemma', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/It%C3%B4%27s_lemma",
    prerequisites=["chain_rule", "derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="geometric_brownian",
    content=(
        "Geometric Brownian motion (GBM) models stock prices: "
        "dS = mu*S dt + sigma*S dW, where mu is the drift and sigma "
        "is the volatility. Solution: S_t = S_0 * exp((mu - sigma^2/2)*t "
        "+ sigma*W_t). The log returns are normally distributed."
    ),
    example=(
        "S_0=100, mu=0.05, sigma=0.2, t=1, W_1=0.5. "
        "S_1 = 100*exp((0.05-0.02)*1 + 0.2*0.5) = 100*exp(0.13) "
        "= 100*1.1388 = 113.88."
    ),
    tier=7,
    domain="stochastic_calculus",
    source="Wikipedia contributors, 'Geometric Brownian motion', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Geometric_Brownian_motion",
    prerequisites=["ito_lemma"],
))

register_atom(Atom(
    atom_type="formula",
    name="black_scholes",
    content=(
        "The Black-Scholes formula prices European call options: "
        "C = S*N(d1) - K*exp(-r*T)*N(d2), where "
        "d1 = (ln(S/K) + (r + sigma^2/2)*T) / (sigma*sqrt(T)), "
        "d2 = d1 - sigma*sqrt(T), and N is the standard normal CDF. "
        "S is the stock price, K the strike, r the risk-free rate, "
        "T time to expiry, sigma the volatility."
    ),
    example=(
        "S=100, K=100, r=0.05, sigma=0.2, T=1. "
        "d1 = (0 + 0.07)/0.2 = 0.35, d2 = 0.15. "
        "N(0.35)=0.6368, N(0.15)=0.5596. "
        "C = 100*0.6368 - 100*0.9512*0.5596 = 63.68 - 53.24 = 10.44."
    ),
    tier=7,
    domain="stochastic_calculus",
    source="Wikipedia contributors, 'Black-Scholes model', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model",
    prerequisites=["geometric_brownian"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="sde_euler",
    content=(
        "The Euler-Maruyama method numerically solves stochastic "
        "differential equations dX = a(X) dt + b(X) dW. Discretisation: "
        "X_{n+1} = X_n + a(X_n)*dt + b(X_n)*sqrt(dt)*Z_n, "
        "where Z_n ~ N(0,1). Strong order of convergence is 0.5."
    ),
    example=(
        "dX = -X dt + dW, X_0=1, dt=0.1, Z_0=0.5. "
        "X_1 = 1 + (-1)*0.1 + 1*sqrt(0.1)*0.5 "
        "= 1 - 0.1 + 0.1581 = 1.0581."
    ),
    tier=6,
    domain="stochastic_calculus",
    source="Wikipedia contributors, 'Euler-Maruyama method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euler%E2%80%93Maruyama_method",
    prerequisites=["ito_lemma"],
))

register_atom(Atom(
    atom_type="formula",
    name="ornstein_uhlenbeck",
    content=(
        "The Ornstein-Uhlenbeck (OU) process is a mean-reverting SDE: "
        "dX = theta*(mu - X) dt + sigma dW, where theta > 0 is the "
        "rate of mean reversion, mu is the long-run mean, and sigma is "
        "the volatility. Solution: X_t = mu + (X_0 - mu)*exp(-theta*t) "
        "+ sigma*integral_0^t exp(-theta*(t-s)) dW_s."
    ),
    example=(
        "theta=2, mu=5, sigma=1, X_0=3, t=1. "
        "E[X_1] = 5 + (3-5)*exp(-2) = 5 - 2*0.1353 = 4.729. "
        "Var[X_1] = sigma^2/(2*theta) * (1 - exp(-2*theta*t)) "
        "= 0.25 * (1 - e^{-4}) = 0.245."
    ),
    tier=7,
    domain="stochastic_calculus",
    source="Wikipedia contributors, 'Ornstein-Uhlenbeck process', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ornstein%E2%80%93Uhlenbeck_process",
    prerequisites=["ito_lemma"],
))

register_atom(Atom(
    atom_type="definition",
    name="martingale_transform",
    content=(
        "A discrete martingale transform is defined by H_n * (M_n - M_{n-1}), "
        "where H is a predictable process (known at time n-1) and M is a "
        "martingale. The cumulative transform (H . M)_n = sum_{k=1}^n "
        "H_k * (M_k - M_{k-1}) is itself a martingale if H is bounded. "
        "This is the discrete analogue of a stochastic integral."
    ),
    example=(
        "Fair coin: M_n = cumulative sum of +1/-1. "
        "H_n = 1 (constant bet). (H.M)_n = M_n, still a martingale. "
        "E[(H.M)_n] = 0 for all n."
    ),
    tier=7,
    domain="stochastic_calculus",
    source="Wikipedia contributors, 'Martingale (probability theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Martingale_(probability_theory)",
    prerequisites=["markov_chain"],
))
