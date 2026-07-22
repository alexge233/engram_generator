"""Knowledge atoms for mathematical physics, financial mathematics,
and formal verification domains.

Each atom stores the authoritative statement sourced from Wikipedia,
a worked example with known input/output, tier, domain, source
citation, source URL, and prerequisite atoms.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ===================================================================
# Mathematical Physics (tier 6-7)
# ===================================================================

register_atom(Atom(
    atom_type="principle",
    name="action_principle",
    content=(
        "The principle of stationary action (Hamilton's principle) states "
        "that the path taken by a physical system between two states is the "
        "one for which the action integral S = integral of L dt is stationary "
        "(usually a minimum). The action is S = int_{t1}^{t2} L(q, dq/dt, t) dt, "
        "where L = T - V is the Lagrangian. The Euler-Lagrange equation "
        "d/dt (dL/d(dq/dt)) - dL/dq = 0 follows from requiring delta S = 0."
    ),
    example=(
        "Free particle L = (1/2)m*v^2: dL/dv = m*v, dL/dx = 0. "
        "Euler-Lagrange: d/dt(m*v) = 0, so m*a = 0, i.e. constant velocity."
    ),
    tier=6,
    domain="mathematical_physics",
    source="Wikipedia contributors, 'Hamilton's principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hamilton%27s_principle",
    prerequisites=["definite_integral", "derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="variational_derivative",
    content=(
        "The variational (functional) derivative delta F/delta f(x) of a "
        "functional F[f] = int L(f, f', x) dx with respect to f(x) is "
        "delta F/delta f = dL/df - d/dx (dL/df'). This generalises the "
        "ordinary derivative to functionals and is the core tool of the "
        "calculus of variations."
    ),
    example=(
        "F[f] = int_0^1 (f')^2 dx. L = (f')^2, dL/df = 0, dL/df' = 2f'. "
        "delta F/delta f = 0 - d/dx(2f') = -2f''. Setting to zero: f'' = 0, "
        "so f(x) = ax + b."
    ),
    tier=7,
    domain="mathematical_physics",
    source="Wikipedia contributors, 'Functional derivative', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Functional_derivative",
    prerequisites=["derivative", "definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="green_function_ode",
    content=(
        "The Green's function G(x, s) for a linear differential operator L "
        "satisfies L G(x, s) = delta(x - s), where delta is the Dirac delta. "
        "The solution to Lu(x) = f(x) is then u(x) = int G(x, s) f(s) ds. "
        "For the operator L = d^2/dx^2 on [0, 1] with u(0) = u(1) = 0, "
        "G(x, s) = s(1-x) for s <= x and x(1-s) for s > x."
    ),
    example=(
        "L = d^2/dx^2, u(0)=u(1)=0, f(x)=1. "
        "u(x) = int_0^x s(1-x) ds + int_x^1 x(1-s) ds "
        "= (1-x)*x^2/2 + x*(1-x)^2/2 = x(1-x)/2."
    ),
    tier=7,
    domain="mathematical_physics",
    source="Wikipedia contributors, 'Green's function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Green%27s_function",
    prerequisites=["definite_integral", "differential_geometry"],
))

register_atom(Atom(
    atom_type="theorem",
    name="sturm_liouville",
    content=(
        "A Sturm-Liouville problem is a second-order linear ODE of the form "
        "d/dx[p(x) dy/dx] + [q(x) + lambda w(x)] y = 0 on [a,b] with "
        "boundary conditions. The eigenvalues lambda_n are real, the "
        "eigenfunctions y_n form a complete orthogonal set with respect to "
        "the weight function w(x), and any square-integrable function can "
        "be expanded in the eigenfunctions."
    ),
    example=(
        "y'' + lambda y = 0, y(0) = y(pi) = 0. "
        "Solution: y_n = sin(n*x), lambda_n = n^2, n = 1, 2, 3, ... "
        "Eigenfunctions are orthogonal: int_0^pi sin(mx)sin(nx) dx = 0 for m != n."
    ),
    tier=7,
    domain="mathematical_physics",
    source="Wikipedia contributors, 'Sturm-Liouville theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Sturm%E2%80%93Liouville_theory",
    prerequisites=["eigenvalue", "definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="fourier_heat_kernel",
    content=(
        "The heat kernel K(x, t) is the fundamental solution of the heat "
        "equation du/dt = k * d^2u/dx^2 on the real line. It is given by "
        "K(x, t) = 1/sqrt(4*pi*k*t) * exp(-x^2 / (4*k*t)). The solution "
        "for initial condition u(x, 0) = f(x) is the convolution "
        "u(x, t) = int K(x - y, t) f(y) dy."
    ),
    example=(
        "k = 1, t = 1: K(x, 1) = 1/sqrt(4*pi) * exp(-x^2/4). "
        "At x = 0: K(0, 1) = 1/sqrt(4*pi) = 1/(2*sqrt(pi)) = 0.2821."
    ),
    tier=6,
    domain="mathematical_physics",
    source="Wikipedia contributors, 'Heat kernel', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Heat_kernel",
    prerequisites=["heat_equation", "definite_integral"],
))

register_atom(Atom(
    atom_type="definition",
    name="symmetry_generator",
    content=(
        "In Lie theory, a symmetry generator is an element of a Lie algebra "
        "that generates a continuous symmetry transformation via "
        "exponentiation. For a Lie group G with Lie algebra g, the generator "
        "X in g produces the one-parameter subgroup exp(t*X) in G. "
        "For rotations in 2D, the generator is J = [[0,-1],[1,0]], and "
        "exp(theta*J) = [[cos(theta),-sin(theta)],[sin(theta),cos(theta)]]."
    ),
    example=(
        "SO(2) generator J = [[0,-1],[1,0]]. "
        "exp(pi/2 * J) = [[cos(pi/2),-sin(pi/2)],[sin(pi/2),cos(pi/2)]] "
        "= [[0,-1],[1,0]], a 90-degree rotation."
    ),
    tier=7,
    domain="mathematical_physics",
    source="Wikipedia contributors, 'Lie algebra', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lie_algebra",
    prerequisites=["matrix_exponential", "eigenvalue"],
))

register_atom(Atom(
    atom_type="formula",
    name="path_integral_simple",
    content=(
        "The Feynman path integral formulates quantum mechanics as a sum "
        "over all possible paths. The propagator from (x_a, t_a) to "
        "(x_b, t_b) is K = int D[x(t)] exp(i*S[x]/hbar), where S is the "
        "classical action. For a free particle of mass m, the exact "
        "propagator is K = sqrt(m/(2*pi*i*hbar*T)) * exp(i*m*(x_b-x_a)^2 / "
        "(2*hbar*T)), where T = t_b - t_a."
    ),
    example=(
        "Free particle, m=1, hbar=1, T=1, x_a=0, x_b=1: "
        "|K|^2 = 1/(2*pi) * 1 = 0.1592. "
        "The probability density to arrive at x=1 after time T=1."
    ),
    tier=7,
    domain="mathematical_physics",
    source="Wikipedia contributors, 'Path integral formulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Path_integral_formulation",
    prerequisites=["definite_integral", "action_principle"],
))

register_atom(Atom(
    atom_type="definition",
    name="group_representation_physics",
    content=(
        "A representation of a group G on a vector space V is a homomorphism "
        "rho: G -> GL(V), mapping each group element to an invertible linear "
        "map on V. In physics, representations of symmetry groups classify "
        "particles and fields. For SU(2), the spin-j representation has "
        "dimension 2j+1. The fundamental representation (j=1/2) uses 2x2 "
        "Pauli matrices."
    ),
    example=(
        "SU(2), j=1/2: dim = 2*0.5 + 1 = 2. "
        "Generators are sigma_x/2, sigma_y/2, sigma_z/2 where sigma_i are "
        "Pauli matrices. j=1: dim = 3 (vector representation)."
    ),
    tier=7,
    domain="mathematical_physics",
    source="Wikipedia contributors, 'Representation theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Representation_theory",
    prerequisites=["group_axiom_check", "eigenvalue"],
))

# ===================================================================
# Financial Mathematics (tier 4-6)
# ===================================================================

register_atom(Atom(
    atom_type="formula",
    name="portfolio_return",
    content=(
        "The expected return of a portfolio is the weighted average of the "
        "expected returns of its constituent assets: E[R_p] = sum_i w_i * E[R_i], "
        "where w_i is the weight (fraction of capital) invested in asset i "
        "and E[R_i] is the expected return of asset i. Weights must sum to 1."
    ),
    example=(
        "Two assets: w_A=0.6, E[R_A]=0.08; w_B=0.4, E[R_B]=0.12. "
        "E[R_p] = 0.6*0.08 + 0.4*0.12 = 0.048 + 0.048 = 0.096 (9.6%)."
    ),
    tier=4,
    domain="financial_mathematics",
    source="Wikipedia contributors, 'Modern portfolio theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Modern_portfolio_theory",
    prerequisites=["expected_value", "weighted_sum"],
))

register_atom(Atom(
    atom_type="formula",
    name="portfolio_variance",
    content=(
        "The variance of a two-asset portfolio is "
        "sigma_p^2 = w_A^2*sigma_A^2 + w_B^2*sigma_B^2 + 2*w_A*w_B*cov(A,B), "
        "where w_i are weights, sigma_i^2 are individual variances, and "
        "cov(A,B) = rho_AB * sigma_A * sigma_B. Diversification reduces "
        "portfolio variance when correlation rho < 1."
    ),
    example=(
        "w_A=0.5, w_B=0.5, sigma_A=0.2, sigma_B=0.3, rho=0.5. "
        "cov = 0.5*0.2*0.3 = 0.03. "
        "sigma_p^2 = 0.25*0.04 + 0.25*0.09 + 2*0.25*0.03 = 0.01+0.0225+0.015 = 0.0475. "
        "sigma_p = sqrt(0.0475) = 0.2179 (21.8%)."
    ),
    tier=5,
    domain="financial_mathematics",
    source="Wikipedia contributors, 'Modern portfolio theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Modern_portfolio_theory",
    prerequisites=["variance", "correlation"],
))

register_atom(Atom(
    atom_type="formula",
    name="sharpe_ratio",
    content=(
        "The Sharpe ratio measures risk-adjusted return: "
        "S = (E[R_p] - R_f) / sigma_p, where E[R_p] is the expected "
        "portfolio return, R_f is the risk-free rate, and sigma_p is the "
        "portfolio standard deviation. Higher Sharpe ratios indicate better "
        "risk-adjusted performance."
    ),
    example=(
        "E[R_p]=0.12, R_f=0.03, sigma_p=0.15. "
        "S = (0.12 - 0.03) / 0.15 = 0.09/0.15 = 0.6."
    ),
    tier=5,
    domain="financial_mathematics",
    source="Wikipedia contributors, 'Sharpe ratio', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Sharpe_ratio",
    prerequisites=["portfolio_return", "std_dev"],
))

register_atom(Atom(
    atom_type="formula",
    name="option_payoff",
    content=(
        "The payoff of a European call option at expiry is max(S_T - K, 0), "
        "where S_T is the stock price at expiry and K is the strike price. "
        "For a European put, the payoff is max(K - S_T, 0). The profit "
        "equals payoff minus the premium paid."
    ),
    example=(
        "Call option: K=100, premium=5. If S_T=110: payoff = max(110-100,0) = 10, "
        "profit = 10-5 = 5. If S_T=95: payoff = 0, profit = -5."
    ),
    tier=4,
    domain="financial_mathematics",
    source="Wikipedia contributors, 'Option (finance)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Option_(finance)",
    prerequisites=["comparison"],
))

register_atom(Atom(
    atom_type="formula",
    name="binomial_option",
    content=(
        "The binomial option pricing model values options by building a "
        "recombining tree. At each step, the stock moves up by factor u or "
        "down by d = 1/u. The risk-neutral probability is p = (e^(r*dt) - d)/(u - d). "
        "Option value at each node: V = e^(-r*dt) * [p*V_up + (1-p)*V_down]. "
        "Working backwards from expiry gives the present value."
    ),
    example=(
        "S=100, K=100, u=1.1, d=0.9, r=0.05, dt=1. "
        "p = (e^0.05 - 0.9)/(1.1 - 0.9) = (1.0513 - 0.9)/0.2 = 0.7565. "
        "V_up = max(110-100,0) = 10, V_down = max(90-100,0) = 0. "
        "V = e^(-0.05) * (0.7565*10 + 0.2435*0) = 0.9512*7.565 = 7.196."
    ),
    tier=6,
    domain="financial_mathematics",
    source="Wikipedia contributors, 'Binomial options pricing model', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Binomial_options_pricing_model",
    prerequisites=["option_payoff", "expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="var_computation",
    content=(
        "Value at Risk (VaR) at confidence level alpha is the maximum loss "
        "not exceeded with probability alpha over a given time horizon. "
        "For normally distributed returns with mean mu and std sigma, "
        "VaR_alpha = -(mu + z_alpha * sigma) * portfolio_value, where "
        "z_alpha is the alpha-quantile of N(0,1) (e.g. z_0.05 = -1.645)."
    ),
    example=(
        "Portfolio $1M, daily mu=0.001, sigma=0.02, alpha=0.05. "
        "VaR_0.05 = -(0.001 + (-1.645)*0.02) * 1000000 "
        "= -(0.001 - 0.0329) * 1000000 = 0.0319 * 1000000 = $31,900."
    ),
    tier=5,
    domain="financial_mathematics",
    source="Wikipedia contributors, 'Value at risk', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Value_at_risk",
    prerequisites=["z_score", "std_dev"],
))

register_atom(Atom(
    atom_type="formula",
    name="bond_pricing",
    content=(
        "The price of a bond is the present value of all future cash flows: "
        "P = sum_{t=1}^{n} C/(1+y)^t + F/(1+y)^n, where C is the coupon "
        "payment, F is the face value, y is the yield to maturity, and n "
        "is the number of periods."
    ),
    example=(
        "Face $1000, coupon rate 5% annual, 3 years, yield 4%. "
        "C = 50. P = 50/1.04 + 50/1.04^2 + 1050/1.04^3 "
        "= 48.08 + 46.23 + 933.51 = $1027.82."
    ),
    tier=5,
    domain="financial_mathematics",
    source="Wikipedia contributors, 'Bond valuation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bond_valuation",
    prerequisites=["present_value", "summation"],
))

register_atom(Atom(
    atom_type="formula",
    name="duration_bond",
    content=(
        "Macaulay duration is the weighted average time to receive the bond's "
        "cash flows: D = (1/P) * sum_{t=1}^{n} t * CF_t / (1+y)^t, where "
        "CF_t is the cash flow at time t, y is the yield, and P is the bond "
        "price. Modified duration D_mod = D/(1+y) measures price sensitivity "
        "to yield changes: dP/P approx -D_mod * dy."
    ),
    example=(
        "2-year bond, F=1000, C=50, y=0.05. P = 50/1.05 + 1050/1.05^2 "
        "= 47.62 + 952.38 = 1000. D = (1/1000)*(1*47.62 + 2*952.38) "
        "= 1952.38/1000 = 1.952 years. D_mod = 1.952/1.05 = 1.859."
    ),
    tier=5,
    domain="financial_mathematics",
    source="Wikipedia contributors, 'Bond duration', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bond_duration",
    prerequisites=["bond_pricing", "derivative"],
))

# ===================================================================
# Formal Verification (tier 6-7)
# ===================================================================

register_atom(Atom(
    atom_type="definition",
    name="hoare_triple",
    content=(
        "A Hoare triple {P} C {Q} asserts that if precondition P holds "
        "before executing command C, then postcondition Q holds after C "
        "terminates. The assignment axiom states {Q[x/E]} x := E {Q}, "
        "meaning the postcondition with x replaced by E must hold before "
        "the assignment. Sequential composition: if {P} C1 {R} and "
        "{R} C2 {Q}, then {P} C1; C2 {Q}."
    ),
    example=(
        "{x+1 > 0} x := x+1 {x > 0}. "
        "Applying assignment axiom: Q = (x > 0), E = x+1, "
        "Q[x/E] = (x+1 > 0). Precondition x+1 > 0 gives x > -1."
    ),
    tier=6,
    domain="formal_verification",
    source="Wikipedia contributors, 'Hoare logic', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hoare_logic",
    prerequisites=["propositional_eval"],
))

register_atom(Atom(
    atom_type="formula",
    name="wp_calculus",
    content=(
        "The weakest precondition wp(S, Q) is the least restrictive "
        "precondition that guarantees postcondition Q after executing "
        "statement S. For assignment: wp(x := E, Q) = Q[x/E]. "
        "For sequential composition: wp(S1; S2, Q) = wp(S1, wp(S2, Q)). "
        "For conditionals: wp(if B then S1 else S2, Q) = "
        "(B => wp(S1, Q)) and (not B => wp(S2, Q))."
    ),
    example=(
        "wp(x := x+1, x > 5) = (x+1 > 5) = (x > 4). "
        "wp(x := x*2; x := x+1, x > 5) = wp(x := x*2, (x+1 > 5)) "
        "= wp(x := x*2, x > 4) = (2*x > 4) = (x > 2)."
    ),
    tier=6,
    domain="formal_verification",
    source="Wikipedia contributors, 'Predicate transformer semantics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Predicate_transformer_semantics",
    prerequisites=["hoare_triple"],
))

register_atom(Atom(
    atom_type="definition",
    name="loop_invariant_verify",
    content=(
        "A loop invariant I is a property that holds before and after each "
        "iteration of a loop. To verify {P} while B do S {Q} using Hoare "
        "logic, one must show: (1) P => I (invariant established), "
        "(2) {I and B} S {I} (invariant preserved), "
        "(3) I and not B => Q (postcondition follows when loop exits). "
        "Finding loop invariants is generally undecidable."
    ),
    example=(
        "Sum 1..n: {n >= 0} s:=0; i:=1; while i<=n do s:=s+i; i:=i+1 {s = n*(n+1)/2}. "
        "Invariant I: s = (i-1)*i/2 and i <= n+1. "
        "At exit (i = n+1): s = n*(n+1)/2."
    ),
    tier=7,
    domain="formal_verification",
    source="Wikipedia contributors, 'Loop invariant', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Loop_invariant",
    prerequisites=["hoare_triple", "wp_calculus"],
))

register_atom(Atom(
    atom_type="definition",
    name="ctl_model_check",
    content=(
        "Computation Tree Logic (CTL) is a branching-time temporal logic. "
        "CTL formulas combine path quantifiers (A = all paths, E = exists "
        "a path) with temporal operators (X = next, F = eventually, G = "
        "globally, U = until). Model checking verifies whether a Kripke "
        "structure M satisfies a CTL formula phi at state s: M, s |= phi. "
        "CTL model checking runs in O(|phi| * (|S| + |R|)) time."
    ),
    example=(
        "Kripke structure: s0 -> s1 -> s2 (loop at s2). "
        "s0: {p}, s1: {q}, s2: {p,q}. "
        "M, s0 |= EF q? Yes: path s0->s1, q holds at s1. "
        "M, s0 |= AG p? No: p does not hold at s1."
    ),
    tier=7,
    domain="formal_verification",
    source="Wikipedia contributors, 'Computation tree logic', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Computation_tree_logic",
    prerequisites=["propositional_eval", "graph_reach"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="ltl_to_buchi",
    content=(
        "Linear Temporal Logic (LTL) formulas can be translated into "
        "Buchi automata for model checking. The automaton accepts exactly "
        "the infinite words satisfying the LTL formula. Key temporal "
        "operators: X (next), F (finally/eventually), G (globally/always), "
        "U (until). The translation uses a tableau construction, producing "
        "a generalised Buchi automaton that is then degeneralised."
    ),
    example=(
        "LTL formula: F p (eventually p). "
        "Buchi automaton: state q0 (initial), state q1 (accepting). "
        "Transitions: q0 --[not p]--> q0, q0 --[p]--> q1, q1 --[true]--> q1. "
        "Accepts any word where p eventually holds."
    ),
    tier=7,
    domain="formal_verification",
    source="Wikipedia contributors, 'Linear temporal logic', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Linear_temporal_logic",
    prerequisites=["nfa_to_dfa", "propositional_eval"],
))

register_atom(Atom(
    atom_type="definition",
    name="bisimulation_check",
    content=(
        "A bisimulation is a binary relation R between states of two "
        "labelled transition systems such that if (p, q) in R, then: "
        "(1) p and q satisfy the same atomic propositions, "
        "(2) if p --a--> p', there exists q --a--> q' with (p', q') in R, "
        "(3) if q --a--> q', there exists p --a--> p' with (p', q') in R. "
        "Bisimilar systems are observationally equivalent."
    ),
    example=(
        "System 1: s0 --a--> s1 --b--> s2. "
        "System 2: t0 --a--> t1 --b--> t2. "
        "R = {(s0,t0), (s1,t1), (s2,t2)} is a bisimulation. "
        "The systems are bisimilar."
    ),
    tier=6,
    domain="formal_verification",
    source="Wikipedia contributors, 'Bisimulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bisimulation",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="abstraction_refinement",
    content=(
        "Counterexample-guided abstraction refinement (CEGAR) is an "
        "iterative model checking technique. Steps: (1) create an abstract "
        "model, (2) model-check the abstract model, (3) if a counterexample "
        "is found, check if it is spurious, (4) if spurious, refine the "
        "abstraction to eliminate it, (5) repeat until verified or a real "
        "counterexample is found."
    ),
    example=(
        "Abstract model merges states {s1,s2} into abstract state a1. "
        "Model checker finds path a0->a1->a2 violating safety. "
        "Concretisation check: s1->a2 is feasible but s2->a2 is not. "
        "Refine: split a1 into {s1} and {s2}. Re-check."
    ),
    tier=7,
    domain="formal_verification",
    source="Wikipedia contributors, 'Counterexample-guided abstraction refinement', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Counterexample-guided_abstraction_refinement",
    prerequisites=["ctl_model_check"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="invariant_synthesis",
    content=(
        "Invariant synthesis automatically discovers loop invariants or "
        "system invariants for formal verification. Approaches include "
        "abstract interpretation (computing fixpoints over abstract domains), "
        "interpolation (deriving invariants from proof of infeasibility of "
        "error paths), and template-based methods (assuming a parametric "
        "form and solving constraints)."
    ),
    example=(
        "Loop: while x < 10 do x := x + 1. "
        "Template: I = (x <= C) for unknown C. "
        "Init x=0: 0 <= C => C >= 0. "
        "Preserve: x < 10 and x <= C => x+1 <= C => C >= 11. "
        "Exit: x >= 10 and x <= C => C >= 10. "
        "Solution: C = 10, invariant I = (x <= 10)."
    ),
    tier=7,
    domain="formal_verification",
    source="Wikipedia contributors, 'Abstract interpretation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Abstract_interpretation",
    prerequisites=["loop_invariant_verify", "wp_calculus"],
))
