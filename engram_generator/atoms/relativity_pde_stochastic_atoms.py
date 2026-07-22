"""Knowledge atoms for special relativity, PDEs, and stochastic processes.

Covers Lorentz transformations, spacetime geometry, wave/heat/Laplace
equations, and Markov chains, random walks, and Poisson processes.
Each atom includes a worked example with concrete numbers.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Special Relativity (tier 5-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="lorentz_factor",
    content=(
        "The Lorentz factor gamma is defined as "
        "gamma = 1 / sqrt(1 - v^2/c^2), where v is the relative velocity "
        "and c is the speed of light. It appears in all relativistic "
        "transformations and approaches infinity as v approaches c."
    ),
    example=(
        "Given v = 0.8c: gamma = 1/sqrt(1 - 0.64) = 1/sqrt(0.36) "
        "= 1/0.6 = 1.6667"
    ),
    tier=5,
    domain="relativity",
    source="Wikipedia contributors, 'Lorentz factor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lorentz_factor",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="time_dilation",
    content=(
        "Time dilation: a moving clock runs slower by the Lorentz factor. "
        "Delta_t = gamma * Delta_t0, where Delta_t0 is the proper time "
        "(measured in the rest frame) and Delta_t is the dilated time "
        "measured by an observer in relative motion."
    ),
    example=(
        "Given Delta_t0 = 1s, v = 0.6c: gamma = 1/sqrt(1-0.36) = 1.25, "
        "Delta_t = 1.25 * 1 = 1.25s"
    ),
    tier=5,
    domain="relativity",
    source="Wikipedia contributors, 'Time dilation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Time_dilation",
    prerequisites=["lorentz_factor"],
))

register_atom(Atom(
    atom_type="formula",
    name="length_contraction",
    content=(
        "Length contraction: a moving object is measured shorter along "
        "its direction of motion. L = L0 / gamma, where L0 is the "
        "proper length and L is the contracted length."
    ),
    example=(
        "Given L0 = 10m, v = 0.8c: gamma = 5/3, "
        "L = 10 / (5/3) = 6m"
    ),
    tier=5,
    domain="relativity",
    source="Wikipedia contributors, 'Length contraction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Length_contraction",
    prerequisites=["lorentz_factor"],
))

register_atom(Atom(
    atom_type="formula",
    name="relativistic_energy",
    content=(
        "The total relativistic energy of a particle is E = gamma*m*c^2, "
        "where m is the rest mass. The rest energy is E0 = m*c^2. "
        "The kinetic energy is KE = (gamma - 1)*m*c^2."
    ),
    example=(
        "Given m = 1kg, v = 0.6c: gamma = 1.25, "
        "E = 1.25 * 1 * (3e8)^2 = 1.125e17 J"
    ),
    tier=5,
    domain="relativity",
    source="Wikipedia contributors, 'Mass-energy equivalence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mass%E2%80%93energy_equivalence",
    prerequisites=["lorentz_factor", "kinetic_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="spacetime_interval",
    content=(
        "The spacetime interval is an invariant quantity: "
        "ds^2 = -(c*dt)^2 + dx^2 + dy^2 + dz^2 (using -+++ signature). "
        "It is the same for all inertial observers. Timelike if ds^2 < 0, "
        "spacelike if ds^2 > 0, lightlike if ds^2 = 0."
    ),
    example=(
        "Events: dt=5s, dx=3e8m, dy=0, dz=0 (c=3e8 m/s): "
        "ds^2 = -(3e8*5)^2 + (3e8)^2 = -2.25e18 + 9e16 = -2.16e18 "
        "(timelike)"
    ),
    tier=5,
    domain="relativity",
    source="Wikipedia contributors, 'Spacetime', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Spacetime#Spacetime_interval",
    prerequisites=["pythagorean"],
))

register_atom(Atom(
    atom_type="formula",
    name="lorentz_transform",
    content=(
        "The Lorentz transformation relates coordinates between two "
        "inertial frames moving at relative velocity v along x: "
        "x' = gamma*(x - v*t), t' = gamma*(t - v*x/c^2). "
        "These reduce to the Galilean transformation for v << c."
    ),
    example=(
        "Given x=1e9m, t=2s, v=0.5c (1.5e8 m/s): gamma=1.1547, "
        "x' = 1.1547*(1e9 - 1.5e8*2) = 1.1547*7e8 = 8.083e8 m"
    ),
    tier=6,
    domain="relativity",
    source="Wikipedia contributors, 'Lorentz transformation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lorentz_transformation",
    prerequisites=["lorentz_factor"],
))

register_atom(Atom(
    atom_type="formula",
    name="velocity_addition",
    content=(
        "Relativistic velocity addition: if object moves at u' in frame S' "
        "which moves at v relative to S, the velocity in S is "
        "u = (u' + v) / (1 + u'*v/c^2). This ensures no combined "
        "velocity exceeds c."
    ),
    example=(
        "Given u' = 0.7c, v = 0.8c: "
        "u = (0.7 + 0.8)c / (1 + 0.56) = 1.5c/1.56 = 0.9615c"
    ),
    tier=5,
    domain="relativity",
    source="Wikipedia contributors, 'Velocity-addition formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Velocity-addition_formula",
    prerequisites=["lorentz_factor"],
))

register_atom(Atom(
    atom_type="formula",
    name="four_momentum",
    content=(
        "The four-momentum of a particle is p^mu = (E/c, p_x, p_y, p_z) "
        "where E = gamma*m*c^2 and p = gamma*m*v. The invariant mass "
        "satisfies E^2 = (pc)^2 + (mc^2)^2."
    ),
    example=(
        "Given m=0.511 MeV/c^2 (electron), v=0.9c: gamma=2.294, "
        "E = 2.294*0.511 = 1.172 MeV, p = 2.294*0.511*0.9/c = 1.055 MeV/c"
    ),
    tier=6,
    domain="relativity",
    source="Wikipedia contributors, 'Four-momentum', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Four-momentum",
    prerequisites=["lorentz_factor", "relativistic_energy"],
))


# =========================================================================
# Partial Differential Equations (tier 6-7)
# =========================================================================

register_atom(Atom(
    atom_type="definition",
    name="classify_pde",
    content=(
        "A second-order linear PDE A*u_xx + 2B*u_xy + C*u_yy + ... = 0 "
        "is classified by the discriminant D = B^2 - A*C: "
        "elliptic if D < 0 (e.g. Laplace), parabolic if D = 0 "
        "(e.g. heat), hyperbolic if D > 0 (e.g. wave)."
    ),
    example=(
        "u_xx + u_yy = 0: A=1, B=0, C=1, D = 0 - 1 = -1 < 0, "
        "so elliptic (Laplace equation)"
    ),
    tier=6,
    domain="pde",
    source="Wikipedia contributors, 'Partial differential equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Partial_differential_equation#Classification",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="heat_equation",
    content=(
        "The heat equation is u_t = alpha * u_xx, where alpha = k/(rho*c_p) "
        "is the thermal diffusivity. Solution on infinite rod with initial "
        "condition u(x,0) = f(x) is given by convolution with the heat "
        "kernel G(x,t) = exp(-x^2/(4*alpha*t)) / sqrt(4*pi*alpha*t)."
    ),
    example=(
        "1D rod, alpha=1, u(x,0)=delta(0): "
        "u(x,t) = exp(-x^2/(4t)) / sqrt(4*pi*t). "
        "At x=1, t=1: u = exp(-0.25)/sqrt(4*pi) = 0.2197"
    ),
    tier=6,
    domain="pde",
    source="Wikipedia contributors, 'Heat equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Heat_equation",
    prerequisites=["derivative", "definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="wave_equation_1d",
    content=(
        "The 1D wave equation is u_tt = c^2 * u_xx, where c is the "
        "wave speed. D'Alembert's solution: u(x,t) = f(x-ct) + g(x+ct) "
        "for right- and left-travelling waves."
    ),
    example=(
        "c=2, f(s)=sin(s), g=0: u(x,t) = sin(x - 2t). "
        "At x=pi, t=pi/4: u = sin(pi - pi/2) = sin(pi/2) = 1"
    ),
    tier=6,
    domain="pde",
    source="Wikipedia contributors, 'Wave equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Wave_equation",
    prerequisites=["derivative", "second_derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="laplace_equation",
    content=(
        "Laplace's equation is nabla^2 u = 0, i.e. u_xx + u_yy = 0 "
        "in 2D. Solutions are harmonic functions. In polar coordinates: "
        "u(r,theta) = sum (a_n*r^n + b_n*r^{-n})(c_n*cos(n*theta) + "
        "d_n*sin(n*theta))."
    ),
    example=(
        "Verify u = ln(sqrt(x^2+y^2)) is harmonic: "
        "u_xx = (y^2-x^2)/(x^2+y^2)^2, u_yy = (x^2-y^2)/(x^2+y^2)^2, "
        "u_xx + u_yy = 0. Confirmed."
    ),
    tier=7,
    domain="pde",
    source="Wikipedia contributors, 'Laplace\\'s equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Laplace%27s_equation",
    prerequisites=["partial_derivative"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="method_of_characteristics",
    content=(
        "The method of characteristics converts a first-order PDE "
        "a*u_x + b*u_y = c into an ODE along characteristic curves "
        "dx/a = dy/b = du/c. The solution is constant along each "
        "characteristic."
    ),
    example=(
        "u_t + 2*u_x = 0, u(x,0) = sin(x): characteristics are "
        "x = 2t + x0, so u(x,t) = sin(x - 2t). "
        "At x=pi, t=pi/4: u = sin(pi/2) = 1"
    ),
    tier=7,
    domain="pde",
    source="Wikipedia contributors, 'Method of characteristics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Method_of_characteristics",
    prerequisites=["classify_pde"],
))

register_atom(Atom(
    atom_type="formula",
    name="greens_function",
    content=(
        "Green's function G(x,x') satisfies L*G = delta(x-x'), where L "
        "is a linear differential operator. The solution to L*u = f is "
        "u(x) = integral G(x,x')*f(x') dx'. For the 1D Poisson equation "
        "-u'' = f on [0,1] with u(0)=u(1)=0: G(x,x') = x'*(1-x) for "
        "x' <= x, and x*(1-x') for x' > x."
    ),
    example=(
        "1D Poisson -u''=1 on [0,1], u(0)=u(1)=0: "
        "u(x) = integral_0^1 G(x,x') dx' = x(1-x)/2. "
        "At x=0.5: u = 0.5*0.5/2 = 0.125"
    ),
    tier=7,
    domain="pde",
    source="Wikipedia contributors, 'Green\\'s function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Green%27s_function",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="fourier_transform_pde",
    content=(
        "The Fourier transform converts a PDE to an ODE in frequency "
        "space: F{u_xx} = -k^2 * F{u}, F{u_t} = d/dt F{u}. Solve "
        "the ODE, then inverse transform. For the heat equation "
        "u_t = alpha*u_xx: F{u}(k,t) = F{u0}(k) * exp(-alpha*k^2*t)."
    ),
    example=(
        "Heat equation, u(x,0) = exp(-x^2): "
        "F{u0}(k) = sqrt(pi)*exp(-k^2/4), "
        "F{u}(k,t) = sqrt(pi)*exp(-k^2(1+4t)/4). "
        "Result: u(x,t) = exp(-x^2/(1+4t))/sqrt(1+4t)"
    ),
    tier=7,
    domain="pde",
    source="Wikipedia contributors, 'Fourier transform', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fourier_transform",
    prerequisites=["definite_integral", "heat_equation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="finite_difference",
    content=(
        "Finite difference method approximates derivatives on a grid: "
        "u'(x) ~ (u(x+h) - u(x-h))/(2h) (central difference), "
        "u''(x) ~ (u(x+h) - 2u(x) + u(x-h))/h^2. For the heat "
        "equation: u_j^{n+1} = u_j^n + r*(u_{j+1}^n - 2u_j^n + u_{j-1}^n) "
        "where r = alpha*dt/dx^2. Stable when r <= 0.5."
    ),
    example=(
        "Heat equation, alpha=1, dx=0.1, dt=0.005: "
        "r = 1*0.005/0.01 = 0.5 (stable). "
        "u_j^{n+1} = u_j^n + 0.5*(u_{j+1}^n - 2*u_j^n + u_{j-1}^n)"
    ),
    tier=6,
    domain="pde",
    source="Wikipedia contributors, 'Finite difference method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Finite_difference_method",
    prerequisites=["derivative"],
))


# =========================================================================
# Stochastic Processes (tier 5-7)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="random_walk",
    content=(
        "A simple random walk on the integers: at each step, move +1 "
        "with probability p or -1 with probability q = 1-p. After n "
        "steps, E[S_n] = n*(2p-1) and Var[S_n] = 4npq. The probability "
        "of returning to the origin is 1 for p=0.5 (recurrent) and < 1 "
        "for p != 0.5 (transient)."
    ),
    example=(
        "Fair coin walk (p=0.5), n=100 steps: "
        "E[S_100] = 100*(2*0.5-1) = 0, "
        "Var[S_100] = 4*100*0.25 = 100, SD = 10"
    ),
    tier=5,
    domain="stochastic",
    source="Wikipedia contributors, 'Random walk', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Random_walk",
    prerequisites=["expected_value", "variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="markov_stationary",
    content=(
        "A stationary distribution pi of a Markov chain with transition "
        "matrix P satisfies pi*P = pi and sum(pi) = 1. For an ergodic "
        "chain, the stationary distribution is unique and equals the "
        "long-run fraction of time in each state."
    ),
    example=(
        "P = [[0.7, 0.3], [0.4, 0.6]]: solve pi*P = pi. "
        "pi_1*0.7 + pi_2*0.4 = pi_1, pi_1 + pi_2 = 1. "
        "0.3*pi_1 = 0.4*pi_2, pi = [4/7, 3/7] = [0.5714, 0.4286]"
    ),
    tier=5,
    domain="stochastic",
    source="Wikipedia contributors, 'Markov chain', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Markov_chain#Stationary_distribution_relation_to_eigenvectors_and_simplices",
    prerequisites=["markov_chain"],
))

register_atom(Atom(
    atom_type="formula",
    name="markov_absorption",
    content=(
        "In an absorbing Markov chain, the fundamental matrix is "
        "N = (I - Q)^{-1}, where Q is the transient-to-transient "
        "submatrix. Expected steps to absorption from state i is "
        "the i-th row sum of N. Absorption probabilities are B = N*R, "
        "where R is the transient-to-absorbing submatrix."
    ),
    example=(
        "Gambler's ruin: states {0,1,2,3}, 0 and 3 absorbing, "
        "p=0.5. Q = [[0.5,0.5],[0.5,0.5]] for states {1,2}. "
        "N = (I-Q)^{-1} = [[2,1],[1,2]]. Expected steps from "
        "state 1: 2+1 = 3"
    ),
    tier=6,
    domain="stochastic",
    source="Wikipedia contributors, 'Absorbing Markov chain', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Absorbing_Markov_chain",
    prerequisites=["markov_stationary", "matrix_inverse"],
))

register_atom(Atom(
    atom_type="formula",
    name="birth_death",
    content=(
        "A birth-death process has transition rates: birth rate "
        "lambda_n (state n to n+1) and death rate mu_n (state n to n-1). "
        "The stationary distribution satisfies detailed balance: "
        "pi_n * lambda_n = pi_{n+1} * mu_{n+1}, giving "
        "pi_n = pi_0 * prod(lambda_k/mu_{k+1}, k=0..n-1)."
    ),
    example=(
        "M/M/1 queue: lambda=2, mu=3. "
        "rho = lambda/mu = 2/3. "
        "pi_n = (1-rho)*rho^n = (1/3)*(2/3)^n. "
        "pi_0 = 1/3, pi_1 = 2/9, pi_2 = 4/27"
    ),
    tier=6,
    domain="stochastic",
    source="Wikipedia contributors, 'Birth-death process', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Birth%E2%80%93death_process",
    prerequisites=["markov_stationary"],
))

register_atom(Atom(
    atom_type="formula",
    name="poisson_process",
    content=(
        "A Poisson process with rate lambda: the number of events in "
        "time t follows Poisson(lambda*t). Inter-arrival times are "
        "Exp(lambda). P(N(t) = k) = (lambda*t)^k * exp(-lambda*t) / k!. "
        "E[N(t)] = lambda*t, Var[N(t)] = lambda*t."
    ),
    example=(
        "Rate lambda=3 events/hour, t=2 hours: "
        "E[N(2)] = 6. P(N(2)=4) = 6^4*exp(-6)/4! "
        "= 1296*0.00248/24 = 0.1339"
    ),
    tier=5,
    domain="stochastic",
    source="Wikipedia contributors, 'Poisson point process', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Poisson_point_process",
    prerequisites=["poisson_dist"],
))

register_atom(Atom(
    atom_type="formula",
    name="brownian_motion",
    content=(
        "Standard Brownian motion (Wiener process) W(t) has: W(0) = 0, "
        "independent increments, W(t) - W(s) ~ N(0, t-s) for t > s. "
        "E[W(t)] = 0, Var[W(t)] = t, Cov[W(s),W(t)] = min(s,t). "
        "Sample paths are continuous but nowhere differentiable."
    ),
    example=(
        "W(t) at t=4: E[W(4)] = 0, Var[W(4)] = 4, SD = 2. "
        "P(W(4) > 3) = P(Z > 3/2) = 1 - Phi(1.5) = 0.0668"
    ),
    tier=6,
    domain="stochastic",
    source="Wikipedia contributors, 'Wiener process', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Wiener_process",
    prerequisites=["random_walk"],
))

register_atom(Atom(
    atom_type="definition",
    name="martingale_check",
    content=(
        "A stochastic process {X_n} is a martingale with respect to "
        "filtration {F_n} if: E[|X_n|] < inf for all n, and "
        "E[X_{n+1} | F_n] = X_n (fair game property). A submartingale "
        "has E[X_{n+1} | F_n] >= X_n, supermartingale has <=."
    ),
    example=(
        "Fair random walk S_n = sum X_i where P(X_i=+1) = P(X_i=-1) = 0.5: "
        "E[S_{n+1} | S_1,...,S_n] = S_n + E[X_{n+1}] = S_n + 0 = S_n. "
        "Martingale confirmed."
    ),
    tier=7,
    domain="stochastic",
    source="Wikipedia contributors, 'Martingale (probability theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Martingale_(probability_theory)",
    prerequisites=["random_walk", "expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="renewal_theory",
    content=(
        "In renewal theory, if inter-arrival times X_i are i.i.d. with "
        "mean mu, the renewal function m(t) = E[N(t)] satisfies "
        "m(t)/t -> 1/mu as t -> inf (elementary renewal theorem). "
        "The key renewal theorem gives the long-run rate of renewals."
    ),
    example=(
        "Light bulbs with mean lifetime mu=1000 hours: "
        "after t=10000 hours, expected replacements "
        "m(t) ~ t/mu = 10000/1000 = 10 bulbs"
    ),
    tier=7,
    domain="stochastic",
    source="Wikipedia contributors, 'Renewal theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Renewal_theory",
    prerequisites=["poisson_process"],
))
