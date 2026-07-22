"""Knowledge atoms for crypto deep, topology deep2, PDE deep, functional analysis ext."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── CRYPTO DEEP ───────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="lattice_svp",
    content=(
        "The Shortest Vector Problem (SVP) asks for the shortest nonzero "
        "vector in a lattice L = {Bx : x in Z^n}. It is believed to be "
        "hard even for quantum computers, making it the basis for "
        "post-quantum cryptographic schemes like NTRU and Kyber."
    ),
    example=(
        "Given basis B = [[4,1],[0,3]], lattice vectors include (4,1), "
        "(0,3), (4,4), (-4,-1). Shortest nonzero: (0,3) with norm 3."
    ),
    tier=6, domain="cryptography",
    source="Wikipedia contributors, 'Lattice problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lattice_problem",
    prerequisites=["linear_equation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="lwe_encrypt",
    content=(
        "Learning With Errors (LWE): given a secret s in Z_q^n, samples "
        "(a_i, b_i = <a_i, s> + e_i mod q) where e_i is small noise. "
        "Encryption: choose random r, compute u = sum(r_i * a_i), "
        "v = sum(r_i * b_i) + floor(q/2)*m. Decryption recovers m from "
        "v - <u, s> mod q being close to 0 or floor(q/2)."
    ),
    example=(
        "q=17, n=2, s=(3,5), a=(7,2), e=1: b = 7*3+2*5+1 mod 17 = "
        "32 mod 17 = 15. Encrypt m=1: v = 15 + 8 = 23 mod 17 = 6."
    ),
    tier=6, domain="cryptography",
    source="Wikipedia contributors, 'Learning with errors', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Learning_with_errors",
    prerequisites=["modular", "matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="ntru_keygen",
    content=(
        "NTRU: key generation picks small polynomials f, g in Z[x]/(x^N-1). "
        "Public key h = p*g*f_q^{-1} mod q where f_q is f inverse mod q. "
        "Security relies on the hardness of finding short vectors in "
        "NTRU lattices."
    ),
    example=(
        "N=7, q=29, p=3: f = 1+x+x^5, g = -1+x^2+x^3. Compute "
        "f_q = f^{-1} mod (x^7-1, 29), then h = 3*g*f_q mod 29."
    ),
    tier=6, domain="cryptography",
    source="Wikipedia contributors, 'NTRUEncrypt', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/NTRUEncrypt",
    prerequisites=["polynomial_eval", "modular"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="secret_sharing_threshold",
    content=(
        "Shamir's Secret Sharing: to share secret s among n parties with "
        "threshold t, construct random polynomial p(x) of degree t-1 with "
        "p(0) = s. Each party i gets share (i, p(i)). Any t shares can "
        "reconstruct s via Lagrange interpolation."
    ),
    example=(
        "Secret s=42, t=3, n=5: p(x) = 42 + 3x + 7x^2. Shares: "
        "(1,52), (2,76), (3,114), (4,166), (5,232). Any 3 shares "
        "reconstruct p(0) = 42."
    ),
    tier=5, domain="cryptography",
    source="Wikipedia contributors, 'Shamir%27s secret sharing', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="commitment_pedersen",
    content=(
        "Pedersen commitment: commit to value m with randomness r as "
        "C = g^m * h^r mod p, where g, h are generators of a group of "
        "prime order q. The commitment is computationally binding and "
        "perfectly hiding."
    ),
    example=(
        "p=23, q=11, g=2, h=9, m=5, r=3: C = 2^5 * 9^3 mod 23 = "
        "32 * 729 mod 23 = 9 * 18 mod 23 = 162 mod 23 = 1."
    ),
    tier=5, domain="cryptography",
    source="Wikipedia contributors, 'Commitment scheme', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Commitment_scheme",
    prerequisites=["modular", "exponentiation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="oblivious_transfer",
    content=(
        "1-out-of-2 Oblivious Transfer: sender has messages m0, m1. "
        "Receiver wants m_b without revealing b. Uses public key crypto: "
        "receiver generates keys, sender encrypts both messages, receiver "
        "can only decrypt one. Sender learns nothing about b."
    ),
    example=(
        "Sender has m0='hello', m1='world'. Receiver wants m1. "
        "After OT protocol, receiver gets 'world', sender doesn't know "
        "which message was retrieved."
    ),
    tier=6, domain="cryptography",
    source="Wikipedia contributors, 'Oblivious transfer', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Oblivious_transfer",
    prerequisites=["rsa_encrypt"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="garbled_circuit",
    content=(
        "Yao's Garbled Circuits: one party garbles a boolean circuit by "
        "encrypting each gate's truth table with random keys. The other "
        "party evaluates the circuit without learning intermediate values. "
        "Combined with OT, enables secure two-party computation."
    ),
    example=(
        "AND gate with inputs a, b: garble creates 4 ciphertexts. "
        "Evaluator with keys k_a=1, k_b=0 can decrypt only the entry "
        "for (1,0), getting key for output=0."
    ),
    tier=6, domain="cryptography",
    source="Wikipedia contributors, 'Garbled circuit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Garbled_circuit",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="hash_chain",
    content=(
        "A hash chain applies a hash function iteratively: h_n = H(h_{n-1}). "
        "Starting from seed s, the chain is s, H(s), H(H(s)), ... "
        "Used in one-time passwords (S/Key), blockchain proof-of-work, "
        "and time-stamping. Verification: given h_n, compute H^k(h_{n-k}) "
        "and check equality."
    ),
    example=(
        "H = SHA-256 truncated to 4 hex chars, seed = 'abc': "
        "h0 = 'abc', h1 = H('abc') = 'ba78', h2 = H('ba78') = '9f3c'. "
        "To verify h2 from h0: H(H('abc')) = '9f3c'. Match."
    ),
    tier=4, domain="cryptography",
    source="Wikipedia contributors, 'Hash chain', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hash_chain",
    prerequisites=["fibonacci"],
))

# ── TOPOLOGY DEEP2 ────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="cw_complex_euler",
    content=(
        "For a finite CW complex with c_k cells of dimension k, the "
        "Euler characteristic is chi = sum((-1)^k * c_k). This equals "
        "the alternating sum of Betti numbers: chi = sum((-1)^k * b_k)."
    ),
    example=(
        "Torus: 1 vertex (c_0=1), 2 edges (c_1=2), 1 face (c_2=1). "
        "chi = 1 - 2 + 1 = 0. Betti numbers b_0=1, b_1=2, b_2=1: "
        "chi = 1 - 2 + 1 = 0. Match."
    ),
    tier=6, domain="topology",
    source="Wikipedia contributors, 'CW complex', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/CW_complex",
    prerequisites=["euler_characteristic"],
))

register_atom(Atom(
    atom_type="theorem",
    name="van_kampen",
    content=(
        "Van Kampen's theorem: if X = U1 union U2 where U1, U2, and "
        "U1 cap U2 are path-connected and open, then pi_1(X) is the "
        "amalgamated free product pi_1(U1) *_{pi_1(U1 cap U2)} pi_1(U2). "
        "This computes fundamental groups from simpler pieces."
    ),
    example=(
        "Figure-eight (wedge of two circles): U1 covers one loop plus "
        "a bit of the other, U2 covers the other loop plus overlap. "
        "pi_1(U1) = Z, pi_1(U2) = Z, U1 cap U2 contractible. "
        "pi_1(figure-eight) = Z * Z (free group on 2 generators)."
    ),
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Seifert-van Kampen theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Seifert%E2%80%93van_Kampen_theorem",
    prerequisites=["fundamental_group"],
))

register_atom(Atom(
    atom_type="theorem",
    name="homology_sphere",
    content=(
        "The homology groups of the n-sphere S^n are: H_0(S^n) = Z, "
        "H_n(S^n) = Z, and H_k(S^n) = 0 for k != 0, n. This follows "
        "from the Mayer-Vietoris sequence or cellular homology."
    ),
    example=(
        "S^2 (2-sphere): H_0 = Z (connected), H_1 = 0, H_2 = Z "
        "(has a 'cavity'). Euler characteristic: 1 - 0 + 1 = 2."
    ),
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Homology (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Homology_(mathematics)",
    prerequisites=["homology_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="suspension",
    content=(
        "The suspension SX of a topological space X is the quotient "
        "(X x [0,1]) / ~ where (x,0) ~ (y,0) and (x,1) ~ (y,1) for "
        "all x, y. It collapses the top and bottom to points. "
        "Key property: H_k(SX) = H_{k-1}(X) for k >= 1."
    ),
    example=(
        "Suspension of S^1 (circle): SS^1 = S^2 (sphere). "
        "H_1(S^1) = Z maps to H_2(SS^1) = H_2(S^2) = Z."
    ),
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Suspension (topology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Suspension_(topology)",
    prerequisites=["homology_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="mapping_cone",
    content=(
        "The mapping cone C_f of a continuous map f: X -> Y is the "
        "quotient (X x [0,1]) union_f Y, identifying (x,1) with f(x). "
        "It fits in a cofiber sequence X -> Y -> C_f and yields a "
        "long exact sequence in homology."
    ),
    example=(
        "f: S^1 -> D^2 (inclusion of boundary): C_f = D^2/S^1 = S^2. "
        "The mapping cone of the inclusion is homeomorphic to S^2."
    ),
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Mapping cone (topology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mapping_cone_(topology)",
    prerequisites=["homology_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="borsuk_ulam",
    content=(
        "Borsuk-Ulam theorem: for any continuous function f: S^n -> R^n, "
        "there exists a point x in S^n such that f(x) = f(-x). "
        "Equivalently, no continuous odd function S^n -> S^{n-1} exists."
    ),
    example=(
        "n=1: any continuous f: S^1 -> R has antipodal points with "
        "equal value. E.g. temperature on the equator: some pair of "
        "diametrically opposite points have the same temperature."
    ),
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Borsuk-Ulam theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Borsuk%E2%80%93Ulam_theorem",
    prerequisites=["continuity_topological"],
))

register_atom(Atom(
    atom_type="theorem",
    name="lefschetz_fixed_point",
    content=(
        "Lefschetz fixed-point theorem: if f: X -> X is a continuous map "
        "on a compact triangulable space and the Lefschetz number "
        "L(f) = sum((-1)^k * tr(f_*k)) != 0, then f has a fixed point."
    ),
    example=(
        "f: S^2 -> S^2, degree 2: f_*0 = id (tr=1), f_*1 = 0 (tr=0), "
        "f_*2 = 2*id (tr=2). L(f) = 1 - 0 + 2 = 3 != 0, so f has a "
        "fixed point."
    ),
    tier=7, domain="topology",
    source="Wikipedia contributors, 'Lefschetz fixed-point theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lefschetz_fixed-point_theorem",
    prerequisites=["homology_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="covering_degree",
    content=(
        "A covering map p: E -> B has degree n if each point b in B has "
        "exactly n preimages. The degree equals the index "
        "[pi_1(B) : p_*(pi_1(E))]. For the universal cover, "
        "degree = |pi_1(B)|."
    ),
    example=(
        "p: R -> S^1, p(t) = e^{2*pi*i*t}: each point of S^1 has "
        "infinitely many preimages (degree = infinity). "
        "p: S^1 -> S^1, p(z) = z^3: degree 3, each point has 3 preimages."
    ),
    tier=6, domain="topology",
    source="Wikipedia contributors, 'Covering space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Covering_space",
    prerequisites=["fundamental_group"],
))

# ── PDE DEEP ──────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="schrodinger_pde",
    content=(
        "Time-dependent Schrodinger equation: i*hbar * d(psi)/dt = "
        "H*psi, where H = -hbar^2/(2m) * nabla^2 + V(x) is the "
        "Hamiltonian. For a free particle: psi(x,t) = A*exp(i(kx - wt))."
    ),
    example=(
        "Free particle, 1D: psi(x,t) = exp(i(kx - hbar*k^2*t/(2m))). "
        "Verify: i*hbar * (-i*hbar*k^2/(2m)) * psi = hbar^2*k^2/(2m) * psi "
        "= H*psi. Correct."
    ),
    tier=6, domain="pde",
    source="Wikipedia contributors, 'Schrodinger equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation",
    prerequisites=["wave_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="diffusion_equation",
    content=(
        "The diffusion equation: du/dt = D * nabla^2 u, where D is the "
        "diffusion coefficient. In 1D: du/dt = D * d^2u/dx^2. "
        "Fundamental solution: u(x,t) = (1/sqrt(4*pi*D*t)) * "
        "exp(-x^2/(4*D*t))."
    ),
    example=(
        "D=1, initial delta at origin: u(x,1) = (1/sqrt(4*pi)) * "
        "exp(-x^2/4). At x=0: u(0,1) = 1/sqrt(4*pi) = 0.2821."
    ),
    tier=5, domain="pde",
    source="Wikipedia contributors, 'Diffusion equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Diffusion_equation",
    prerequisites=["heat_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="laplace_cylindrical",
    content=(
        "Laplace's equation in cylindrical coordinates: "
        "(1/r)*d/dr(r*du/dr) + (1/r^2)*d^2u/dtheta^2 + d^2u/dz^2 = 0. "
        "Separation of variables gives Bessel functions R(r) = J_n(kr), "
        "trigonometric Theta(theta), and exponentials Z(z)."
    ),
    example=(
        "Axially symmetric (no theta dependence, no z dependence): "
        "u(r) = A*ln(r) + B. Boundary: u(1) = 0, u(2) = 5. "
        "0 = B, 5 = A*ln(2). A = 5/ln(2) = 7.213. u(r) = 7.213*ln(r)."
    ),
    tier=7, domain="pde",
    source="Wikipedia contributors, 'Laplace%27s equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Laplace%27s_equation",
    prerequisites=["laplace_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="wave_damped",
    content=(
        "Damped wave equation: d^2u/dt^2 + 2*gamma*du/dt = c^2*nabla^2 u, "
        "where gamma is the damping coefficient. Solutions are damped "
        "oscillations: u = exp(-gamma*t) * f(x - v*t) where "
        "v = sqrt(c^2 - gamma^2) for underdamped case."
    ),
    example=(
        "c=3, gamma=1, 1D: v = sqrt(9-1) = sqrt(8) = 2.828. "
        "Solution: u(x,t) = exp(-t) * sin(x - 2.828t). Amplitude "
        "decays as exp(-t)."
    ),
    tier=6, domain="pde",
    source="Wikipedia contributors, 'Wave equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Wave_equation",
    prerequisites=["wave_equation_1d"],
))

register_atom(Atom(
    atom_type="formula",
    name="nonlinear_pde_burger",
    content=(
        "Burgers' equation: du/dt + u*du/dx = nu*d^2u/dx^2, where nu "
        "is viscosity. The Cole-Hopf transformation u = -2*nu*(d(ln phi)/dx) "
        "linearises it to the heat equation for phi."
    ),
    example=(
        "Inviscid (nu=0): du/dt + u*du/dx = 0. Initial u(x,0) = sin(x). "
        "Characteristics: x = x0 + sin(x0)*t. Shock forms at t = 1."
    ),
    tier=7, domain="pde",
    source="Wikipedia contributors, 'Burgers%27 equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Burgers%27_equation",
    prerequisites=["advection_equation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="fem_1d",
    content=(
        "Finite Element Method in 1D: discretise domain [a,b] into elements, "
        "approximate u(x) = sum(u_j * phi_j(x)) with piecewise linear "
        "basis functions phi_j. The weak form integral(u'*v') = integral(f*v) "
        "yields a tridiagonal stiffness matrix Ku = F."
    ),
    example=(
        "-u'' = 1 on [0,1], u(0)=u(1)=0, 3 elements (h=1/3): "
        "K = (1/h)*[[2,-1,0],[-1,2,-1],[0,-1,2]] = 3*[[2,-1,0],...]. "
        "F = h*[1,1,1] = [1/3,1/3,1/3]. Solve Ku=F for interior nodes."
    ),
    tier=6, domain="pde",
    source="Wikipedia contributors, 'Finite element method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Finite_element_method",
    prerequisites=["gaussian_elimination"],
))

register_atom(Atom(
    atom_type="formula",
    name="stability_cfl",
    content=(
        "The Courant-Friedrichs-Lewy (CFL) condition for explicit "
        "finite difference schemes: C = c*dt/dx <= C_max, where c is "
        "wave speed, dt is time step, dx is spatial step. For the 1D "
        "wave equation with central differences, C_max = 1."
    ),
    example=(
        "c=2, dx=0.1: dt <= C_max*dx/c = 1*0.1/2 = 0.05. "
        "Using dt=0.04: CFL = 2*0.04/0.1 = 0.8 <= 1. Stable."
    ),
    tier=6, domain="pde",
    source="Wikipedia contributors, 'Courant-Friedrichs-Lewy condition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Courant%E2%80%93Friedrichs%E2%80%93Lewy_condition",
    prerequisites=["wave_equation_1d"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="spectral_method",
    content=(
        "Spectral methods approximate PDE solutions as truncated series "
        "of orthogonal basis functions (Fourier, Chebyshev, Legendre). "
        "For periodic domains, the Fourier spectral method represents "
        "u(x) = sum(u_hat_k * exp(ikx)). Derivatives become algebraic: "
        "du/dx -> ik*u_hat_k."
    ),
    example=(
        "u(x) = sin(3x) on [0, 2*pi]: Fourier coefficients u_hat_3 = -i/2, "
        "u_hat_{-3} = i/2. du/dx: multiply by ik: "
        "3i*(-i/2)*exp(3ix) = (3/2)*exp(3ix). Result: 3*cos(3x). Correct."
    ),
    tier=7, domain="pde",
    source="Wikipedia contributors, 'Spectral method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Spectral_method",
    prerequisites=["fourier_series_compute"],
))

# ── FUNCTIONAL ANALYSIS EXT ───────────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="operator_norm",
    content=(
        "The operator norm of a bounded linear operator T: X -> Y between "
        "normed spaces is ||T|| = sup{||Tx||_Y : ||x||_X <= 1}. "
        "Equivalently, ||T|| = sup(||Tx||/||x||) for x != 0."
    ),
    example=(
        "T: R^2 -> R^2, T(x,y) = (2x, 3y). ||T|| = sup over unit circle: "
        "max of sqrt(4*cos^2(t) + 9*sin^2(t)) = 3 (at t=pi/2)."
    ),
    tier=6, domain="functional_analysis",
    source="Wikipedia contributors, 'Operator norm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Operator_norm",
    prerequisites=["norm_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="spectrum_compute",
    content=(
        "The spectrum sigma(T) of a bounded linear operator T on a "
        "Banach space is the set of lambda in C such that (T - lambda*I) "
        "is not invertible. It contains eigenvalues (point spectrum) "
        "plus continuous and residual spectrum."
    ),
    example=(
        "T = [[2,1],[0,3]] on C^2: det(T - lambda*I) = (2-lambda)(3-lambda). "
        "sigma(T) = {2, 3}. Both are eigenvalues (point spectrum)."
    ),
    tier=6, domain="functional_analysis",
    source="Wikipedia contributors, 'Spectrum (functional analysis)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Spectrum_(functional_analysis)",
    prerequisites=["eigenvalue"],
))

register_atom(Atom(
    atom_type="definition",
    name="resolvent",
    content=(
        "The resolvent of T at lambda is R(lambda, T) = (T - lambda*I)^{-1}, "
        "defined for lambda not in sigma(T). The resolvent set is "
        "rho(T) = C \\ sigma(T). The resolvent satisfies the identity "
        "R(lambda) - R(mu) = (lambda - mu)*R(lambda)*R(mu)."
    ),
    example=(
        "T = [[3,0],[0,5]], lambda = 1: R(1,T) = (T - I)^{-1} = "
        "[[1/2, 0],[0, 1/4]]. ||R(1,T)|| = 1/2 = 1/dist(1, sigma(T))."
    ),
    tier=6, domain="functional_analysis",
    source="Wikipedia contributors, 'Resolvent formalism', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Resolvent_formalism",
    prerequisites=["spectrum_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="compact_integral_operator",
    content=(
        "An integral operator (Tf)(x) = integral(K(x,y)*f(y) dy) with "
        "continuous kernel K on a bounded domain is compact on L^2. "
        "By the spectral theorem for compact self-adjoint operators, "
        "it has countable eigenvalues converging to 0."
    ),
    example=(
        "K(x,y) = min(x,y) on [0,1]: the operator Tf = int_0^1 min(x,y)*f(y)dy "
        "has eigenvalues lambda_n = 1/((n-1/2)^2 * pi^2). "
        "lambda_1 = 4/pi^2 = 0.4053."
    ),
    tier=7, domain="functional_analysis",
    source="Wikipedia contributors, 'Compact operator', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Compact_operator",
    prerequisites=["compact_operator"],
))

register_atom(Atom(
    atom_type="definition",
    name="trace_class",
    content=(
        "A trace-class operator T on a Hilbert space H has finite trace norm: "
        "||T||_1 = tr(sqrt(T*T)) < infinity. The trace tr(T) = sum(<Te_n, e_n>) "
        "is independent of the orthonormal basis {e_n}."
    ),
    example=(
        "T = diag(1/n^2) on l^2: ||T||_1 = sum(1/n^2) = pi^2/6 = 1.6449. "
        "T is trace-class. tr(T) = pi^2/6."
    ),
    tier=6, domain="functional_analysis",
    source="Wikipedia contributors, 'Trace class', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trace_class",
    prerequisites=["operator_norm"],
))

register_atom(Atom(
    atom_type="definition",
    name="weak_convergence",
    content=(
        "A sequence x_n in a Banach space X converges weakly to x if "
        "f(x_n) -> f(x) for all f in X* (the dual space). Weak convergence "
        "is weaker than norm convergence. In Hilbert spaces, "
        "<x_n, y> -> <x, y> for all y."
    ),
    example=(
        "e_n = standard basis in l^2: <e_n, y> = y_n -> 0 for any "
        "y in l^2 (since sum|y_n|^2 < inf). So e_n converges weakly to 0, "
        "but ||e_n|| = 1 (not norm convergent)."
    ),
    tier=6, domain="functional_analysis",
    source="Wikipedia contributors, 'Weak topology', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Weak_topology",
    prerequisites=["dual_space"],
))

register_atom(Atom(
    atom_type="theorem",
    name="closed_graph",
    content=(
        "Closed Graph Theorem: a linear operator T: X -> Y between "
        "Banach spaces is bounded if and only if its graph "
        "G(T) = {(x, Tx) : x in X} is closed in X x Y."
    ),
    example=(
        "T: C[0,1] -> C[0,1], Tf = f' (differentiation). T is unbounded "
        "(||f_n'||/||f_n|| can be arbitrarily large). The graph is not "
        "closed in C[0,1] x C[0,1] (uniform convergence doesn't imply "
        "convergence of derivatives)."
    ),
    tier=7, domain="functional_analysis",
    source="Wikipedia contributors, 'Closed graph theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Closed_graph_theorem_(functional_analysis)",
    prerequisites=["banach_space_check"],
))

register_atom(Atom(
    atom_type="definition",
    name="lp_space_norm",
    content=(
        "The L^p space norm for 1 <= p < infinity is "
        "||f||_p = (integral |f|^p dx)^{1/p}. For p = infinity, "
        "||f||_inf = ess sup |f|. The space l^p consists of sequences "
        "with sum |x_n|^p < infinity."
    ),
    example=(
        "f(x) = x on [0,1]: ||f||_2 = (integral_0^1 x^2 dx)^{1/2} = "
        "(1/3)^{1/2} = 0.5774. ||f||_1 = integral_0^1 x dx = 0.5."
    ),
    tier=5, domain="functional_analysis",
    source="Wikipedia contributors, 'Lp space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lp_space",
    prerequisites=["norm_compute"],
))
