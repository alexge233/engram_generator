"""Knowledge atoms for control systems, game theory, and advanced optics."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Control Systems (Ext) ─────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="root_locus",
    content=(
        "The root locus is the plot of the closed-loop poles of a "
        "transfer function H(s) = KG(s)/(1+KG(s)) as the gain K varies "
        "from 0 to infinity. The locus starts at the open-loop poles "
        "(K=0) and terminates at the open-loop zeros (K->inf). Branches "
        "on the real axis exist to the left of an odd number of real "
        "poles and zeros."
    ),
    example=(
        "G(s) = 1/((s+1)(s+3)): poles at s=-1, s=-3. "
        "Root locus on real axis between -1 and -3. "
        "Breakaway point: s = -2. At K=1: characteristic "
        "equation s^2+4s+3+1=0, s^2+4s+4=0, s=-2 (double pole)."
    ),
    tier=6,
    domain="control_theory",
    source="Wikipedia contributors, 'Root locus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Root_locus",
    prerequisites=["transfer_function_sys"],
))

register_atom(Atom(
    atom_type="formula",
    name="gain_margin",
    content=(
        "Gain margin is the factor by which the gain can be increased "
        "before the system becomes unstable. It is measured at the "
        "phase crossover frequency (where phase = -180 degrees). "
        "GM = 1/|G(jw_pc)| or in dB: GM_dB = -20*log10(|G(jw_pc)|). "
        "A positive gain margin (in dB) indicates stability."
    ),
    example=(
        "G(jw) at phase crossover w_pc=2 rad/s: |G(j2)| = 0.5. "
        "GM = 1/0.5 = 2 = 6.02 dB. System can tolerate 2x gain "
        "increase before instability."
    ),
    tier=6,
    domain="control_theory",
    source="Wikipedia contributors, 'Gain margin', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gain_margin",
    prerequisites=["bode_magnitude"],
))

register_atom(Atom(
    atom_type="formula",
    name="phase_margin",
    content=(
        "Phase margin is the additional phase lag required to bring "
        "the system to the verge of instability. It is measured at the "
        "gain crossover frequency (where |G(jw)| = 1). "
        "PM = 180 + angle(G(jw_gc)). A positive phase margin indicates "
        "stability; typically PM > 45 degrees is desired."
    ),
    example=(
        "At gain crossover w_gc=1 rad/s: angle(G(j1)) = -135 degrees. "
        "PM = 180 + (-135) = 45 degrees. Adequate stability margin."
    ),
    tier=6,
    domain="control_theory",
    source="Wikipedia contributors, 'Phase margin', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Phase_margin",
    prerequisites=["bode_magnitude"],
))

register_atom(Atom(
    atom_type="theorem",
    name="controllability",
    content=(
        "A linear system (A, B) is controllable if the controllability "
        "matrix C = [B, AB, A^2B, ..., A^(n-1)B] has full rank "
        "(rank = n, the state dimension). This means every state can "
        "be reached from any initial state using suitable inputs. "
        "Also known as the Kalman rank condition."
    ),
    example=(
        "A = [[0,1],[0,0]], B = [[0],[1]]: "
        "C = [B, AB] = [[0,1],[1,0]]. "
        "det(C) = -1 != 0, rank = 2 = n. System is controllable."
    ),
    tier=6,
    domain="control_theory",
    source="Wikipedia contributors, 'Controllability', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Controllability",
    prerequisites=["transfer_function_sys"],
))

register_atom(Atom(
    atom_type="theorem",
    name="observability",
    content=(
        "A linear system (A, C) is observable if the observability "
        "matrix O = [C; CA; CA^2; ...; CA^(n-1)] has full rank "
        "(rank = n). This means every initial state can be determined "
        "from the output history. Dual of controllability."
    ),
    example=(
        "A = [[0,1],[-2,-3]], C = [1,0]: "
        "O = [[1,0],[0,1]]. "
        "det(O) = 1 != 0, rank = 2 = n. System is observable."
    ),
    tier=6,
    domain="control_theory",
    source="Wikipedia contributors, 'Observability', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Observability",
    prerequisites=["controllability"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="pole_placement",
    content=(
        "Pole placement (or full state feedback) designs a gain "
        "matrix K such that the closed-loop system x' = (A-BK)x has "
        "eigenvalues at specified locations. Requires the system to be "
        "controllable. The characteristic polynomial of (A-BK) is set "
        "equal to the desired characteristic polynomial."
    ),
    example=(
        "A = [[0,1],[0,0]], B = [[0],[1]], desired poles at -1,-2: "
        "desired polynomial: (s+1)(s+2) = s^2+3s+2. "
        "K = [2, 3] gives A-BK with eigenvalues -1, -2."
    ),
    tier=6,
    domain="control_theory",
    source="Wikipedia contributors, 'Full state feedback', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Full_state_feedback",
    prerequisites=["controllability"],
))

register_atom(Atom(
    atom_type="formula",
    name="steady_state_error",
    content=(
        "The steady-state error of a unity feedback system is "
        "e_ss = lim(s->0) s*R(s)/(1+G(s)) for a reference input R(s). "
        "For a step input R(s)=1/s: e_ss = 1/(1+Kp) where Kp is the "
        "position error constant Kp = lim(s->0) G(s). For a type-1 "
        "system, Kp = infinity and e_ss = 0 for step inputs."
    ),
    example=(
        "G(s) = 10/(s+2): Kp = lim(s->0) 10/(s+2) = 5. "
        "Step response e_ss = 1/(1+5) = 1/6 = 0.1667."
    ),
    tier=5,
    domain="control_theory",
    source="Wikipedia contributors, 'Steady state error', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Steady-state_error",
    prerequisites=["transfer_function_sys"],
))

register_atom(Atom(
    atom_type="formula",
    name="second_order_response",
    content=(
        "A second-order system G(s) = wn^2/(s^2 + 2*zeta*wn*s + wn^2) "
        "has natural frequency wn and damping ratio zeta. "
        "Underdamped (0<zeta<1): oscillatory response with overshoot "
        "Mp = exp(-pi*zeta/sqrt(1-zeta^2)) * 100%. "
        "Settling time ts ~= 4/(zeta*wn). "
        "Peak time tp = pi/(wn*sqrt(1-zeta^2))."
    ),
    example=(
        "wn=10 rad/s, zeta=0.5: "
        "Mp = exp(-pi*0.5/sqrt(0.75)) * 100% = exp(-1.814) * 100% = 16.3%. "
        "ts = 4/(0.5*10) = 0.8 s. "
        "tp = pi/(10*sqrt(0.75)) = 0.363 s."
    ),
    tier=5,
    domain="control_theory",
    source="Wikipedia contributors, 'Damping', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Damping",
    prerequisites=["transfer_function_sys"],
))

# ── Game Theory (Deep) ────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="mixed_strategy_ne",
    content=(
        "A mixed strategy Nash equilibrium assigns probabilities to "
        "each player's pure strategies such that each player is "
        "indifferent between their strategies given the opponent's mix. "
        "For a 2x2 game, player 1 mixes to make player 2 indifferent: "
        "p*a + (1-p)*c = p*b + (1-p)*d, solving for p."
    ),
    example=(
        "Matching pennies: [[1,-1],[-1,1]] vs [[-1,1],[1,-1]]. "
        "Player 1 mixes p=0.5 H, 0.5 T. "
        "Player 2 mixes q=0.5 H, 0.5 T. "
        "Expected payoff for both = 0."
    ),
    tier=5,
    domain="game_theory",
    source="Wikipedia contributors, 'Nash equilibrium', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nash_equilibrium",
    prerequisites=["nash_equilibrium"],
))

register_atom(Atom(
    atom_type="theorem",
    name="zero_sum_game",
    content=(
        "A zero-sum game is one where each outcome's payoffs sum to "
        "zero: what one player gains, the other loses. The minimax "
        "theorem (von Neumann) states that every finite two-person "
        "zero-sum game has an optimal mixed strategy and a well-defined "
        "value v = max_p min_q p^T A q = min_q max_p p^T A q."
    ),
    example=(
        "Payoff matrix A = [[3,0],[5,1]]: "
        "Row player maximin: min(row 1)=0, min(row 2)=1, maximin=1. "
        "Col player minimax: max(col 1)=5, max(col 2)=1, minimax=1. "
        "Saddle point at (row 2, col 2), value = 1."
    ),
    tier=4,
    domain="game_theory",
    source="Wikipedia contributors, 'Zero-sum game', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Zero-sum_game",
    prerequisites=["payoff_matrix"],
))

register_atom(Atom(
    atom_type="definition",
    name="prisoners_dilemma",
    content=(
        "The prisoner's dilemma is a canonical game where two rational "
        "players each have an incentive to defect even though mutual "
        "cooperation yields a better outcome for both. Payoffs: "
        "mutual cooperate (R,R), mutual defect (P,P), "
        "one defects (T,S) with T>R>P>S and 2R>T+S. "
        "The unique Nash equilibrium is (Defect, Defect)."
    ),
    example=(
        "Payoffs: R=3, P=1, T=5, S=0. "
        "Matrix: [[3,3],[0,5]] / [[5,0],[1,1]]. "
        "Dominant strategy for both: Defect. NE = (D,D) with payoff (1,1). "
        "Pareto optimal: (C,C) with (3,3), but not an equilibrium."
    ),
    tier=3,
    domain="game_theory",
    source="Wikipedia contributors, 'Prisoner's dilemma', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Prisoner%27s_dilemma",
    prerequisites=["dominant_strategy"],
))

register_atom(Atom(
    atom_type="definition",
    name="chicken_game",
    content=(
        "The game of chicken (or hawk-dove) models two players heading "
        "for a collision where swerving is safer but straight wins if "
        "the opponent swerves. Two pure NE: one swerves, other goes "
        "straight. One mixed NE. Payoffs: both straight (crash) worst "
        "for both; one swerves (chicken loses face); both swerve (draw)."
    ),
    example=(
        "Payoffs: both swerve (3,3), one straight one swerve (5,1) or "
        "(1,5), both straight (0,0). "
        "Pure NE: (Straight, Swerve) and (Swerve, Straight). "
        "Mixed NE: each goes straight with p = 2/5."
    ),
    tier=4,
    domain="game_theory",
    source="Wikipedia contributors, 'Chicken (game)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chicken_(game)",
    prerequisites=["nash_equilibrium"],
))

register_atom(Atom(
    atom_type="definition",
    name="battle_of_sexes",
    content=(
        "Battle of the Sexes is a coordination game where both players "
        "prefer to coordinate but disagree on which outcome is better. "
        "Two pure NE (one at each player's preferred outcome) and one "
        "mixed NE. Models situations requiring coordination with "
        "conflicting preferences."
    ),
    example=(
        "Payoffs: (Opera,Opera)=(3,2), (Fight,Fight)=(2,3), "
        "mismatch=(0,0). Pure NE: (O,O) and (F,F). "
        "Mixed NE: Player 1 plays O with p=3/5, Player 2 plays O with q=2/5."
    ),
    tier=4,
    domain="game_theory",
    source="Wikipedia contributors, 'Battle of the sexes (game theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Battle_of_the_sexes_(game_theory)",
    prerequisites=["nash_equilibrium"],
))

register_atom(Atom(
    atom_type="definition",
    name="pareto_efficiency",
    content=(
        "An outcome is Pareto efficient (Pareto optimal) if no player "
        "can be made better off without making another player worse off. "
        "An outcome x Pareto dominates y if every player weakly prefers "
        "x and at least one strictly prefers it. The Pareto frontier is "
        "the set of all non-dominated outcomes."
    ),
    example=(
        "Outcomes: A=(4,3), B=(3,4), C=(2,2), D=(5,1). "
        "A dominates C (4>2 and 3>2). B dominates C. "
        "Pareto frontier: {A, B, D}. C is Pareto inefficient."
    ),
    tier=4,
    domain="game_theory",
    source="Wikipedia contributors, 'Pareto efficiency', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pareto_efficiency",
    prerequisites=["payoff_matrix"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="backward_induction",
    content=(
        "Backward induction solves extensive-form (sequential) games by "
        "reasoning from the end of the game tree backwards. At each "
        "decision node, the player chooses the action maximising their "
        "payoff given that subsequent players also play optimally. "
        "The resulting strategy profile is the subgame perfect equilibrium."
    ),
    example=(
        "Two-stage game: Player 1 chooses L or R. If L, Player 2 "
        "chooses A(3,2) or B(1,4). If R, payoff (2,2). "
        "Backward: P2 picks A (2>4? No, picks B giving 4). "
        "P1: L->1, R->2. P1 picks R. SPE outcome: (R) with payoff (2,2)."
    ),
    tier=5,
    domain="game_theory",
    source="Wikipedia contributors, 'Backward induction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Backward_induction",
    prerequisites=["extensive_form"],
))

register_atom(Atom(
    atom_type="formula",
    name="auction_first_price",
    content=(
        "In a first-price sealed-bid auction with n bidders having "
        "independent private values uniformly distributed on [0,1], "
        "the symmetric Bayesian Nash equilibrium bidding strategy is "
        "b(v) = v*(n-1)/n. Each bidder shades their bid below their "
        "value to balance winning probability against overpaying."
    ),
    example=(
        "3 bidders, value v=0.9: b(0.9) = 0.9 * 2/3 = 0.6. "
        "Bidder bids 0.6, not their true value 0.9. "
        "Expected revenue to seller: (n-1)/(n+1) = 2/4 = 0.5."
    ),
    tier=5,
    domain="game_theory",
    source="Wikipedia contributors, 'First-price sealed-bid auction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/First-price_sealed-bid_auction",
    prerequisites=["nash_equilibrium"],
))

# ── Optics (Deep) ─────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="michelson_interferometer",
    content=(
        "A Michelson interferometer splits a beam into two paths and "
        "recombines them. Constructive interference occurs when the "
        "path difference is an integer number of wavelengths: "
        "2d = m*lambda, where d is the mirror displacement and m is "
        "the fringe order. Intensity: I = I_0 * cos^2(pi*d/lambda)."
    ),
    example=(
        "lambda=632.8 nm (HeNe laser), 100 fringes counted: "
        "d = 100 * 632.8e-9 / 2 = 31.64 um mirror displacement."
    ),
    tier=5,
    domain="optics",
    source="Wikipedia contributors, 'Michelson interferometer', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Michelson_interferometer",
    prerequisites=["double_slit"],
))

register_atom(Atom(
    atom_type="formula",
    name="fabry_perot",
    content=(
        "A Fabry-Perot interferometer uses two parallel partially "
        "reflective surfaces. The transmission function is an Airy "
        "function: T = 1/(1 + F*sin^2(delta/2)), where "
        "F = 4R/(1-R)^2 is the coefficient of finesse, R is "
        "reflectance, and delta = 4*pi*n*d*cos(theta)/lambda. "
        "Free spectral range: FSR = lambda^2/(2*n*d)."
    ),
    example=(
        "R=0.9, d=1 cm, n=1, lambda=500 nm: "
        "F = 4*0.9/0.01 = 360. "
        "Finesse = pi*sqrt(F)/2 = pi*sqrt(360)/2 = 29.8. "
        "FSR = (500e-9)^2 / (2*0.01) = 1.25e-14 m = 0.0125 pm."
    ),
    tier=6,
    domain="optics",
    source="Wikipedia contributors, 'Fabry-Perot interferometer', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fabry%E2%80%93P%C3%A9rot_interferometer",
    prerequisites=["michelson_interferometer"],
))

register_atom(Atom(
    atom_type="formula",
    name="gaussian_beam",
    content=(
        "A Gaussian beam has an intensity profile I(r) = I_0 * "
        "(w_0/w(z))^2 * exp(-2r^2/w(z)^2) where w(z) = w_0 * "
        "sqrt(1 + (z/z_R)^2) is the beam radius and z_R = pi*w_0^2/lambda "
        "is the Rayleigh range. The beam divergence half-angle is "
        "theta = lambda/(pi*w_0)."
    ),
    example=(
        "lambda=1064 nm, w_0=0.5 mm: "
        "z_R = pi*(0.5e-3)^2 / 1064e-9 = 0.738 m. "
        "At z=1 m: w(1) = 0.5e-3 * sqrt(1 + (1/0.738)^2) = 0.74 mm. "
        "Divergence: theta = 1064e-9 / (pi*0.5e-3) = 0.677 mrad."
    ),
    tier=6,
    domain="optics",
    source="Wikipedia contributors, 'Gaussian beam', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gaussian_beam",
    prerequisites=["double_slit"],
))

register_atom(Atom(
    atom_type="formula",
    name="coherence_length",
    content=(
        "The coherence length is the propagation distance over which "
        "a coherent wave maintains a specified degree of coherence. "
        "For a source with spectral width delta_lambda: "
        "L_c = lambda^2 / delta_lambda. Equivalently, "
        "L_c = c / delta_nu where delta_nu is the frequency bandwidth. "
        "Longer coherence length means more monochromatic source."
    ),
    example=(
        "HeNe laser: lambda=632.8 nm, delta_nu=1.5 GHz: "
        "L_c = 3e8 / 1.5e9 = 0.2 m = 20 cm. "
        "White light: delta_lambda=300 nm: "
        "L_c = (550e-9)^2 / 300e-9 = 1.0 um."
    ),
    tier=5,
    domain="optics",
    source="Wikipedia contributors, 'Coherence length', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coherence_length",
    prerequisites=["double_slit"],
))

register_atom(Atom(
    atom_type="formula",
    name="optical_fiber_modes",
    content=(
        "The number of modes in a step-index optical fiber is determined "
        "by the V number: V = (2*pi*a/lambda) * sqrt(n1^2 - n2^2), "
        "where a is the core radius, n1 and n2 are core and cladding "
        "refractive indices. Single-mode condition: V < 2.405. "
        "Number of modes ~= V^2/2 for large V."
    ),
    example=(
        "a=25 um, lambda=850 nm, n1=1.48, n2=1.46: "
        "NA = sqrt(1.48^2 - 1.46^2) = sqrt(0.0588) = 0.2425. "
        "V = 2*pi*25e-6*0.2425 / 850e-9 = 44.9. "
        "Modes ~= 44.9^2/2 = 1008 modes (multimode)."
    ),
    tier=5,
    domain="optics",
    source="Wikipedia contributors, 'Fiber optics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Optical_fiber",
    prerequisites=["snells_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="jones_matrix",
    content=(
        "Jones calculus represents polarised light as a 2-component "
        "complex vector and optical elements as 2x2 matrices. "
        "Horizontal polariser: [[1,0],[0,0]]. "
        "Quarter-wave plate (fast axis horizontal): [[1,0],[0,i]]. "
        "Half-wave plate: [[1,0],[0,-1]]. "
        "Output = M * input_vector. Applicable only to fully polarised light."
    ),
    example=(
        "45-degree polarised light E = (1/sqrt(2))[1,1]^T through "
        "horizontal polariser [[1,0],[0,0]]: "
        "E_out = (1/sqrt(2))[1,0]^T. "
        "Intensity: |E_out|^2 = 1/2 (Malus's law, cos^2(45) = 0.5)."
    ),
    tier=5,
    domain="optics",
    source="Wikipedia contributors, 'Jones calculus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Jones_calculus",
    prerequisites=["double_slit"],
))

register_atom(Atom(
    atom_type="formula",
    name="abbe_diffraction_limit",
    content=(
        "The Abbe diffraction limit gives the minimum resolvable "
        "feature size in optical microscopy: d = lambda / (2 * NA), "
        "where NA = n * sin(theta) is the numerical aperture. "
        "For visible light (lambda ~= 550 nm) and high NA oil "
        "immersion (NA = 1.4): d ~= 200 nm."
    ),
    example=(
        "lambda=550 nm, NA=1.4 (oil immersion): "
        "d = 550e-9 / (2*1.4) = 196 nm. "
        "Air objective NA=0.95: d = 550e-9 / (2*0.95) = 289 nm."
    ),
    tier=4,
    domain="optics",
    source="Wikipedia contributors, 'Diffraction-limited system', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Diffraction-limited_system",
    prerequisites=["single_slit_diffraction"],
))

register_atom(Atom(
    atom_type="formula",
    name="prism_dispersion",
    content=(
        "A prism separates white light into its component wavelengths "
        "because the refractive index n depends on wavelength "
        "(dispersion). The angular dispersion is d(delta)/d(lambda) = "
        "(dn/d(lambda)) * (2*sin(A/2)) / sqrt(1 - n^2*sin^2(A/2)), "
        "where A is the prism angle and delta is the deviation angle. "
        "The Cauchy equation approximates: n(lambda) = B + C/lambda^2."
    ),
    example=(
        "Crown glass: B=1.5220, C=0.00459 um^2. "
        "At 486 nm (blue): n = 1.5220 + 0.00459/0.486^2 = 1.5414. "
        "At 656 nm (red): n = 1.5220 + 0.00459/0.656^2 = 1.5327. "
        "Dispersion: dn = 0.0087 over visible range."
    ),
    tier=5,
    domain="optics",
    source="Wikipedia contributors, 'Dispersion (optics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dispersion_(optics)",
    prerequisites=["snells_law"],
))
