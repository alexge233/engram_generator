"""Knowledge atoms for automata ext, diffeq ext, and trigonometry ext."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ---------------------------------------------------------------------------
# Automata Theory Ext (tiers 4-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="mealy_machine",
    content=(
        "A Mealy machine is a finite-state transducer where outputs depend "
        "on the current state AND input: delta(s, i) = (s', o). Formally "
        "(Q, Sigma, Gamma, delta, lambda, q0) where lambda(s, i) = output. "
        "Outputs are associated with transitions, not states."
    ),
    example=(
        "States {S0, S1}, input {0, 1}, output {a, b}. "
        "delta(S0, 0) = (S0, a), delta(S0, 1) = (S1, b), "
        "delta(S1, 0) = (S0, b), delta(S1, 1) = (S1, a). "
        "Input 101: output = b, a, b."
    ),
    tier=4,
    domain="automata_ext",
    source="Wikipedia contributors, 'Mealy machine', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mealy_machine",
    prerequisites=["dfa_accept"],
))

register_atom(Atom(
    atom_type="definition",
    name="moore_machine",
    content=(
        "A Moore machine is a finite-state transducer where outputs depend "
        "only on the current state: lambda(s) = output. Formally "
        "(Q, Sigma, Gamma, delta, lambda, q0). Every Moore machine can be "
        "converted to an equivalent Mealy machine and vice versa."
    ),
    example=(
        "States {S0, S1}, input {0, 1}. lambda(S0)=a, lambda(S1)=b. "
        "delta(S0, 0)=S0, delta(S0, 1)=S1, delta(S1, 0)=S0, delta(S1, 1)=S1. "
        "Input 101: states S0->S1->S0->S1, output = a, b, a, b."
    ),
    tier=4,
    domain="automata_ext",
    source="Wikipedia contributors, 'Moore machine', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Moore_machine",
    prerequisites=["dfa_accept"],
))

register_atom(Atom(
    atom_type="definition",
    name="transducer",
    content=(
        "A finite-state transducer (FST) maps input sequences to output "
        "sequences. It generalises both Mealy and Moore machines. Can be "
        "deterministic or non-deterministic. Applications: morphological "
        "analysis, speech processing, protocol conversion."
    ),
    example=(
        "Binary incrementer FST: reads LSB first, carries. "
        "Input 0110 (=6): output 1110 (=7). States track carry bit."
    ),
    tier=5,
    domain="automata_ext",
    source="Wikipedia contributors, 'Finite-state transducer', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Finite-state_transducer",
    prerequisites=["mealy_machine"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="dfa_minimization",
    content=(
        "DFA minimisation finds the smallest DFA recognising the same "
        "language. Hopcroft's algorithm partitions states by distinguishability: "
        "two states are equivalent if no input string leads one to accept "
        "and the other to reject. Start with {accepting, non-accepting} "
        "partition and refine. O(n log n) time."
    ),
    example=(
        "DFA with 4 states, {q0,q2} accept. States q1 and q3 are "
        "equivalent (same transitions, same acceptance). Merge into "
        "3-state minimal DFA."
    ),
    tier=5,
    domain="automata_ext",
    source="Wikipedia contributors, 'DFA minimization', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/DFA_minimization",
    prerequisites=["dfa_accept"],
))

register_atom(Atom(
    atom_type="theorem",
    name="pumping_lemma_cfl",
    content=(
        "The pumping lemma for context-free languages: for any CFL L, "
        "there exists p such that any string s in L with |s| >= p can be "
        "written as s = uvwxy where |vwx| <= p, |vx| >= 1, and "
        "uv^i wx^i y is in L for all i >= 0. Used to prove a language "
        "is NOT context-free."
    ),
    example=(
        "L = {a^n b^n c^n : n >= 0} is not CFL. For any pumping "
        "decomposition of a^p b^p c^p, pumping v and x cannot maintain "
        "equal counts of all three symbols."
    ),
    tier=6,
    domain="automata_ext",
    source="Wikipedia contributors, 'Pumping lemma for context-free languages', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pumping_lemma_for_context-free_languages",
    prerequisites=["cfg_derivation"],
))

register_atom(Atom(
    atom_type="definition",
    name="two_stack_pda",
    content=(
        "A two-stack pushdown automaton has two independent stacks and is "
        "equivalent in power to a Turing machine. A standard PDA (one stack) "
        "recognises exactly the context-free languages. The second stack "
        "provides the ability to simulate a tape, making the automaton "
        "Turing-complete."
    ),
    example=(
        "Recognise {a^n b^n c^n}: push a's on stack 1, match b's by "
        "moving from stack 1 to stack 2, match c's by popping stack 2. "
        "Not possible with one stack."
    ),
    tier=6,
    domain="automata_ext",
    source="Wikipedia contributors, 'Pushdown automaton', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pushdown_automaton",
    prerequisites=["pumping_lemma_cfl"],
))

# ---------------------------------------------------------------------------
# Differential Equations Ext (tier 6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="variation_of_parameters",
    content=(
        "Variation of parameters finds a particular solution to a "
        "non-homogeneous linear ODE y'' + p(x)y' + q(x)y = g(x). "
        "Given fundamental solutions y1, y2 of the homogeneous equation, "
        "the particular solution is y_p = -y1*integral(y2*g/W) + "
        "y2*integral(y1*g/W), where W = y1*y2' - y2*y1' is the Wronskian."
    ),
    example=(
        "y'' + y = sec(x). Homogeneous: y1=cos(x), y2=sin(x), W=1. "
        "y_p = -cos(x)*integral(sin(x)*sec(x)) + sin(x)*integral(cos(x)*sec(x)) "
        "= -cos(x)*integral(tan(x)) + sin(x)*integral(1) "
        "= cos(x)*ln|cos(x)| + x*sin(x)."
    ),
    tier=6,
    domain="diffeq_ext",
    source="Wikipedia contributors, 'Variation of parameters', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Variation_of_parameters",
    prerequisites=["integral", "determinant"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="laplace_solve_ode",
    content=(
        "The Laplace transform method solves linear ODEs with constant "
        "coefficients by transforming the ODE to an algebraic equation "
        "in s-domain: L{y'} = sY - y(0), L{y''} = s^2*Y - s*y(0) - y'(0). "
        "Solve for Y(s), then inverse-transform to get y(t)."
    ),
    example=(
        "y'' + 3y' + 2y = 0, y(0)=1, y'(0)=0. "
        "s^2*Y - s + 3(sY-1) + 2Y = 0. Y(s^2+3s+2) = s+3. "
        "Y = (s+3)/((s+1)(s+2)) = 2/(s+1) - 1/(s+2). "
        "y(t) = 2e^{-t} - e^{-2t}."
    ),
    tier=6,
    domain="diffeq_ext",
    source="Wikipedia contributors, 'Laplace transform applied to differential equations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Laplace_transform_applied_to_differential_equations",
    prerequisites=["laplace_transform"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="system_ode_matrix",
    content=(
        "A system of linear ODEs x' = Ax is solved by finding eigenvalues "
        "and eigenvectors of A. If A has distinct eigenvalues lambda_i with "
        "eigenvectors v_i, the general solution is x(t) = sum c_i * e^{lambda_i*t} * v_i. "
        "For repeated eigenvalues, generalised eigenvectors are needed."
    ),
    example=(
        "x' = [[1,1],[0,2]]x. Eigenvalues: 1, 2. Eigenvectors: [1,0], [1,1]. "
        "x(t) = c1*e^t*[1,0] + c2*e^{2t}*[1,1]."
    ),
    tier=6,
    domain="diffeq_ext",
    source="Wikipedia contributors, 'Matrix differential equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Matrix_differential_equation",
    prerequisites=["eigenvalue"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="boundary_value",
    content=(
        "A boundary value problem (BVP) specifies conditions at two or "
        "more points: y'' = f(x, y, y'), y(a)=alpha, y(b)=beta. Unlike "
        "IVPs, existence and uniqueness are not guaranteed. Methods: "
        "shooting method (convert to IVP), finite differences, collocation."
    ),
    example=(
        "y'' = -2, y(0)=0, y(1)=0. General solution: y = -x^2 + c1*x + c2. "
        "y(0)=0: c2=0. y(1)=0: -1+c1=0, c1=1. y = x - x^2."
    ),
    tier=6,
    domain="diffeq_ext",
    source="Wikipedia contributors, 'Boundary value problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Boundary_value_problem",
    prerequisites=["second_derivative"],
))

register_atom(Atom(
    atom_type="theorem",
    name="stability_ode",
    content=(
        "For the linear system x' = Ax, stability is determined by the "
        "eigenvalues of A. Asymptotically stable: all Re(lambda) < 0. "
        "Unstable: any Re(lambda) > 0. Marginally stable: all Re(lambda) <= 0 "
        "with purely imaginary eigenvalues having simple multiplicity. "
        "For nonlinear systems, linearise around equilibria."
    ),
    example=(
        "A = [[-1, 0], [0, -2]]. Eigenvalues: -1, -2. Both negative, "
        "so the origin is asymptotically stable (node)."
    ),
    tier=6,
    domain="diffeq_ext",
    source="Wikipedia contributors, 'Stability theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stability_theory",
    prerequisites=["eigenvalue"],
))

register_atom(Atom(
    atom_type="definition",
    name="exact_ode",
    content=(
        "An ODE M(x,y)dx + N(x,y)dy = 0 is exact if dM/dy = dN/dx. "
        "Then there exists F(x,y) such that dF/dx = M and dF/dy = N, "
        "and the solution is F(x,y) = C. F is found by integrating "
        "M with respect to x (or N with respect to y) and matching."
    ),
    example=(
        "(2xy + 3)dx + (x^2 + 4y)dy = 0. M=2xy+3, N=x^2+4y. "
        "dM/dy=2x, dN/dx=2x. Exact. F = integral(2xy+3)dx = x^2*y+3x+g(y). "
        "dF/dy = x^2+g'(y) = x^2+4y, so g(y)=2y^2. F = x^2*y+3x+2y^2=C."
    ),
    tier=6,
    domain="diffeq_ext",
    source="Wikipedia contributors, 'Exact differential equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exact_differential_equation",
    prerequisites=["partial_derivative"],
))

# ---------------------------------------------------------------------------
# Trigonometry Ext (tiers 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="inverse_trig",
    content=(
        "Inverse trigonometric functions return angles from ratios: "
        "arcsin(x) maps [-1,1] to [-pi/2, pi/2], arccos(x) maps [-1,1] "
        "to [0, pi], arctan(x) maps R to (-pi/2, pi/2). Key identity: "
        "arcsin(x) + arccos(x) = pi/2. arctan(a) + arctan(b) = "
        "arctan((a+b)/(1-ab)) when ab < 1."
    ),
    example="arcsin(0.5) = pi/6 = 30 degrees. arctan(1) = pi/4 = 45 degrees.",
    tier=4,
    domain="trigonometry_ext",
    source="Wikipedia contributors, 'Inverse trigonometric functions', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inverse_trigonometric_functions",
    prerequisites=["sin_cos_eval"],
))

register_atom(Atom(
    atom_type="formula",
    name="hyperbolic_functions",
    content=(
        "Hyperbolic functions are defined via exponentials: "
        "sinh(x) = (e^x - e^{-x})/2, cosh(x) = (e^x + e^{-x})/2, "
        "tanh(x) = sinh(x)/cosh(x). Key identity: cosh^2(x) - sinh^2(x) = 1. "
        "Derivatives: d/dx sinh(x) = cosh(x), d/dx cosh(x) = sinh(x)."
    ),
    example=(
        "sinh(1) = (e - 1/e)/2 = (2.718 - 0.368)/2 = 1.175. "
        "cosh(1) = (e + 1/e)/2 = (2.718 + 0.368)/2 = 1.543. "
        "cosh^2(1) - sinh^2(1) = 2.381 - 1.381 = 1."
    ),
    tier=4,
    domain="trigonometry_ext",
    source="Wikipedia contributors, 'Hyperbolic functions', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hyperbolic_functions",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="trig_equation",
    content=(
        "Trigonometric equations are solved by isolating the trig function "
        "and using inverse functions plus periodicity. For sin(x) = a: "
        "x = arcsin(a) + 2k*pi or x = pi - arcsin(a) + 2k*pi. "
        "For cos(x) = a: x = +/- arccos(a) + 2k*pi. For tan(x) = a: "
        "x = arctan(a) + k*pi."
    ),
    example=(
        "sin(x) = 1/2 on [0, 2*pi]: x = pi/6 or x = 5*pi/6. "
        "cos(2x) = 0: 2x = pi/2 + k*pi, x = pi/4 + k*pi/2."
    ),
    tier=5,
    domain="trigonometry_ext",
    source="Wikipedia contributors, 'Trigonometric equations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trigonometric_equation",
    prerequisites=["inverse_trig"],
))

register_atom(Atom(
    atom_type="formula",
    name="double_angle",
    content=(
        "Double angle formulas: sin(2x) = 2*sin(x)*cos(x), "
        "cos(2x) = cos^2(x) - sin^2(x) = 2*cos^2(x) - 1 = 1 - 2*sin^2(x), "
        "tan(2x) = 2*tan(x) / (1 - tan^2(x)). Half-angle: "
        "sin^2(x/2) = (1-cos(x))/2, cos^2(x/2) = (1+cos(x))/2."
    ),
    example=(
        "x = 30 degrees: sin(60) = 2*sin(30)*cos(30) = 2*0.5*0.866 = 0.866. "
        "cos(60) = 2*cos^2(30) - 1 = 2*0.75 - 1 = 0.5."
    ),
    tier=4,
    domain="trigonometry_ext",
    source="Wikipedia contributors, 'List of trigonometric identities', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/List_of_trigonometric_identities",
    prerequisites=["sin_cos_eval"],
))

register_atom(Atom(
    atom_type="formula",
    name="inverse_hyperbolic",
    content=(
        "Inverse hyperbolic functions: arsinh(x) = ln(x + sqrt(x^2+1)), "
        "arcosh(x) = ln(x + sqrt(x^2-1)) for x >= 1, "
        "artanh(x) = (1/2)*ln((1+x)/(1-x)) for |x| < 1. "
        "These appear in integration of expressions involving sqrt(x^2+/-1)."
    ),
    example=(
        "arsinh(1) = ln(1 + sqrt(2)) = ln(2.414) = 0.8814. "
        "artanh(0.5) = 0.5*ln(3/1) = 0.5*ln(3) = 0.5493."
    ),
    tier=5,
    domain="trigonometry_ext",
    source="Wikipedia contributors, 'Inverse hyperbolic functions', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inverse_hyperbolic_functions",
    prerequisites=["hyperbolic_functions", "logarithm"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="trig_substitution",
    content=(
        "Trigonometric substitution simplifies integrals containing "
        "sqrt(a^2-x^2), sqrt(x^2-a^2), or sqrt(x^2+a^2). Rules: "
        "sqrt(a^2-x^2): set x = a*sin(t). sqrt(x^2+a^2): set x = a*tan(t). "
        "sqrt(x^2-a^2): set x = a*sec(t). After substitution, integrate "
        "the trig expression and convert back."
    ),
    example=(
        "integral(1/sqrt(4-x^2))dx: a=2, x=2sin(t), dx=2cos(t)dt. "
        "integral(2cos(t)/(2cos(t)))dt = t + C = arcsin(x/2) + C."
    ),
    tier=5,
    domain="trigonometry_ext",
    source="Wikipedia contributors, 'Trigonometric substitution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trigonometric_substitution",
    prerequisites=["inverse_trig", "integral"],
))
