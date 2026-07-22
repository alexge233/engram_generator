"""Knowledge atoms for electromagnetism (deep) and combinatorics (deep).

Covers circuit analysis, electromagnetic fields, waveguides,
and combinatorial identities, generating functions, and enumeration.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ───────────────────────────────────────────────────────────────────
# Electromagnetism deep (tier 4-6)
# ───────────────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="parallel_plate_field",
    content=(
        "The electric field between two parallel conducting plates "
        "with surface charge density sigma is E = sigma / epsilon_0, "
        "where epsilon_0 = 8.854e-12 F/m is the permittivity of free "
        "space. For a voltage V across plates separated by distance d, "
        "E = V/d. The field is uniform between the plates and zero "
        "outside (ideal case)."
    ),
    example=(
        "Given V=100V, d=0.02m: E = V/d = 100/0.02 = 5000 V/m"
    ),
    tier=4,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Capacitor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Capacitor",
    prerequisites=["electric_field"],
))

register_atom(Atom(
    atom_type="law",
    name="gauss_sphere",
    content=(
        "Gauss's law applied to a spherical Gaussian surface of "
        "radius r enclosing charge Q gives E * 4*pi*r^2 = Q/epsilon_0, "
        "so E = Q / (4*pi*epsilon_0*r^2) = k*Q/r^2. For a uniformly "
        "charged sphere of total charge Q and radius R: outside (r>R) "
        "the field is E = k*Q/r^2; inside (r<R) the field is "
        "E = k*Q*r/R^3."
    ),
    example=(
        "Given Q=1e-6 C, r=0.5m: "
        "E = 8.99e9 * 1e-6 / 0.25 = 35960 V/m"
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Gauss's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gauss%27s_law",
    prerequisites=["gauss_law", "electric_field"],
))

register_atom(Atom(
    atom_type="formula",
    name="capacitor_network",
    content=(
        "Capacitors in series: 1/C_total = 1/C1 + 1/C2 + ... "
        "Capacitors in parallel: C_total = C1 + C2 + ... "
        "For two capacitors in series: C_total = C1*C2/(C1+C2)."
    ),
    example=(
        "Given C1=4uF, C2=6uF in series: "
        "C_total = 4*6/(4+6) = 24/10 = 2.4 uF"
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Series and parallel circuits', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Series_and_parallel_circuits",
    prerequisites=["capacitance"],
))

register_atom(Atom(
    atom_type="formula",
    name="rc_time_constant",
    content=(
        "The RC time constant tau = R*C determines the charging and "
        "discharging rate of a capacitor. During charging: "
        "V(t) = V0*(1 - e^(-t/tau)). During discharging: "
        "V(t) = V0*e^(-t/tau). After one time constant, the voltage "
        "reaches ~63.2% (charging) or drops to ~36.8% (discharging)."
    ),
    example=(
        "Given R=10kOhm, C=100uF: tau = 10e3 * 100e-6 = 1.0 s. "
        "At t=1s charging from 5V: V = 5*(1-e^(-1)) = 5*0.6321 = 3.1606 V"
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'RC circuit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/RC_circuit",
    prerequisites=["capacitance", "ohms_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="rl_circuit",
    content=(
        "The RL time constant tau = L/R determines the current growth "
        "and decay rate. During energising: I(t) = (V/R)*(1 - e^(-t/tau)). "
        "During de-energising: I(t) = I0*e^(-t/tau). The inductor "
        "opposes changes in current."
    ),
    example=(
        "Given L=0.5H, R=100Ohm: tau = 0.5/100 = 0.005 s = 5 ms. "
        "V=10V, steady-state I = V/R = 0.1 A"
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'RL circuit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/RL_circuit",
    prerequisites=["ohms_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="wheatstone_bridge",
    content=(
        "A Wheatstone bridge is balanced when R1/R2 = R3/R4, "
        "meaning no current flows through the galvanometer. "
        "The unknown resistance Rx = R3*R2/R1. When unbalanced, "
        "the bridge voltage is V_bridge = V_s * (R3/(R3+R4) - R2/(R1+R2))."
    ),
    example=(
        "Given R1=100, R2=200, R3=150, balanced: "
        "Rx = R3*R2/R1 = 150*200/100 = 300 Ohm"
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Wheatstone bridge', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Wheatstone_bridge",
    prerequisites=["ohms_law"],
))

register_atom(Atom(
    atom_type="law",
    name="biot_savart",
    content=(
        "The Biot-Savart law gives the magnetic field dB due to a "
        "current element: dB = (mu_0/4*pi) * I*dl x r_hat / r^2, "
        "where mu_0 = 4*pi*1e-7 T*m/A. For an infinite straight wire: "
        "B = mu_0*I/(2*pi*r)."
    ),
    example=(
        "Given I=5A, r=0.1m (infinite wire): "
        "B = 4*pi*1e-7 * 5 / (2*pi*0.1) = 1e-5 T = 10 uT"
    ),
    tier=6,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Biot-Savart law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Biot%E2%80%93Savart_law",
    prerequisites=["magnetic_force"],
))

register_atom(Atom(
    atom_type="formula",
    name="mutual_inductance",
    content=(
        "Mutual inductance M between two coils quantifies the voltage "
        "induced in one coil by a changing current in the other: "
        "V2 = -M * dI1/dt. For two solenoids with coupling coefficient "
        "k: M = k*sqrt(L1*L2), where 0 <= k <= 1."
    ),
    example=(
        "Given L1=10mH, L2=40mH, k=0.5: "
        "M = 0.5*sqrt(0.01*0.04) = 0.5*0.02 = 0.01 H = 10 mH"
    ),
    tier=6,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Mutual inductance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inductance#Mutual_inductance",
    prerequisites=["faraday_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="skin_depth",
    content=(
        "The skin depth delta is the depth at which the current density "
        "falls to 1/e of its surface value in a conductor carrying AC: "
        "delta = sqrt(2*rho/(omega*mu)), where rho is resistivity, "
        "omega = 2*pi*f is angular frequency, and mu is permeability. "
        "For copper at 60 Hz: delta ~ 8.5 mm."
    ),
    example=(
        "Given rho=1.68e-8 (copper), f=1e6 Hz, mu=4*pi*1e-7: "
        "omega=2*pi*1e6, delta = sqrt(2*1.68e-8/(6.283e6*1.257e-6)) "
        "= sqrt(3.36e-8/7.896e-6) = sqrt(4.255e-3) = 0.0652 mm = 65.2 um"
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Skin effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Skin_effect",
    prerequisites=["ohms_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="waveguide_cutoff",
    content=(
        "The cutoff frequency of a rectangular waveguide for the TE_mn "
        "mode is f_c = (c/2)*sqrt((m/a)^2 + (n/b)^2), where a and b "
        "are the waveguide dimensions (a > b), c is the speed of light, "
        "and m, n are mode indices. The dominant mode is TE_10 with "
        "f_c = c/(2a)."
    ),
    example=(
        "Given a=0.02286m (WR-90), TE_10: "
        "f_c = 3e8/(2*0.02286) = 3e8/0.04572 = 6.562 GHz"
    ),
    tier=6,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Waveguide (electromagnetism)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Waveguide_(electromagnetism)",
    prerequisites=["wave_equation"],
))


# ───────────────────────────────────────────────────────────────────
# Combinatorics deep (tier 3-6)
# ───────────────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="identity",
    name="fibonacci_identity",
    content=(
        "Fibonacci identities include Cassini's identity: "
        "F(n-1)*F(n+1) - F(n)^2 = (-1)^n, and the addition formula: "
        "F(m+n) = F(m)*F(n+1) + F(m-1)*F(n). The Fibonacci sequence "
        "is defined by F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)."
    ),
    example=(
        "Cassini's identity for n=5: F(4)*F(6) - F(5)^2 "
        "= 3*8 - 5^2 = 24 - 25 = -1 = (-1)^5"
    ),
    tier=4,
    domain="combinatorics",
    source="Wikipedia contributors, 'Fibonacci sequence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fibonacci_sequence#Identities",
    prerequisites=["fibonacci"],
))

register_atom(Atom(
    atom_type="formula",
    name="pascal_triangle",
    content=(
        "Pascal's triangle is an arrangement of binomial coefficients "
        "where entry (n, k) = C(n, k) = n!/(k!*(n-k)!). Key properties: "
        "C(n, k) = C(n-1, k-1) + C(n-1, k) (Pascal's rule), "
        "row sum = 2^n, alternating row sum = 0."
    ),
    example=(
        "Row 5: C(5,0)=1, C(5,1)=5, C(5,2)=10, C(5,3)=10, "
        "C(5,4)=5, C(5,5)=1. Sum = 32 = 2^5"
    ),
    tier=3,
    domain="combinatorics",
    source="Wikipedia contributors, 'Pascal's triangle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pascal%27s_triangle",
    prerequisites=["binomial"],
))

register_atom(Atom(
    atom_type="identity",
    name="vandermonde_identity",
    content=(
        "Vandermonde's identity (convolution): "
        "C(m+n, r) = sum_{k=0}^{r} C(m, k)*C(n, r-k). "
        "This counts the number of ways to choose r items from "
        "two groups of sizes m and n."
    ),
    example=(
        "C(5+3, 4) = C(8,4) = 70. "
        "Via Vandermonde: sum C(5,k)*C(3,4-k) for k=1..4 "
        "= C(5,1)*C(3,3) + C(5,2)*C(3,2) + C(5,3)*C(3,1) + C(5,4)*C(3,0) "
        "= 5*1 + 10*3 + 10*3 + 5*1 = 5+30+30+5 = 70"
    ),
    tier=4,
    domain="combinatorics",
    source="Wikipedia contributors, 'Vandermonde's identity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Vandermonde%27s_identity",
    prerequisites=["binomial", "pascal_triangle"],
))

register_atom(Atom(
    atom_type="formula",
    name="exponential_gf",
    content=(
        "The exponential generating function (EGF) for a sequence "
        "{a_n} is E(x) = sum_{n=0}^{inf} a_n * x^n / n!. "
        "Key EGFs: e^x for {1,1,1,...}, e^x-1 for non-empty subsets, "
        "1/(1-x) has OGF for {1,1,1,...}. The EGF for permutations "
        "of n with k cycles is related to unsigned Stirling numbers."
    ),
    example=(
        "EGF for derangements: e^{-x}/(1-x). "
        "Coefficient of x^3/3!: D(3) = 3!(1 - 1 + 1/2 - 1/6) = 6*1/3 = 2"
    ),
    tier=6,
    domain="combinatorics",
    source="Wikipedia contributors, 'Generating function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Generating_function#Exponential_generating_function",
    prerequisites=["taylor_series"],
))

register_atom(Atom(
    atom_type="theorem",
    name="polya_enumeration",
    content=(
        "Polya enumeration theorem counts distinct objects under a "
        "symmetry group G: |colourings|/|G| = (1/|G|) * "
        "sum_{g in G} k^{c(g)}, where c(g) is the number of cycles "
        "in the permutation g and k is the number of colours. "
        "Generalises Burnside's lemma."
    ),
    example=(
        "Colour vertices of a square with 2 colours. "
        "G = {e, r90, r180, r270, h, v, d1, d2} (|G|=8). "
        "Cycle indices: c(e)=4, c(r90)=1, c(r180)=2, c(r270)=1, "
        "c(h)=c(v)=2, c(d1)=c(d2)=3. "
        "Count = (2^4 + 2^1 + 2^2 + 2^1 + 2^2 + 2^2 + 2^3 + 2^3)/8 "
        "= (16+2+4+2+4+4+8+8)/8 = 48/8 = 6"
    ),
    tier=6,
    domain="combinatorics",
    source="Wikipedia contributors, 'Polya enumeration theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/P%C3%B3lya_enumeration_theorem",
    prerequisites=["burnside_counting"],
))

register_atom(Atom(
    atom_type="formula",
    name="recurrence_characteristic",
    content=(
        "A linear recurrence a_n = c1*a_{n-1} + c2*a_{n-2} + ... "
        "has characteristic equation x^k - c1*x^{k-1} - ... - ck = 0. "
        "If roots are r1, r2, ..., rk (distinct), then "
        "a_n = A1*r1^n + A2*r2^n + ... + Ak*rk^n, where constants "
        "are determined by initial conditions."
    ),
    example=(
        "Fibonacci: a_n = a_{n-1} + a_{n-2}. "
        "Characteristic: x^2 - x - 1 = 0. "
        "Roots: (1+sqrt(5))/2 and (1-sqrt(5))/2. "
        "Binet's formula: F(n) = (phi^n - psi^n)/sqrt(5)"
    ),
    tier=5,
    domain="combinatorics",
    source="Wikipedia contributors, 'Recurrence relation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Recurrence_relation#Solving_linear_recurrence_relations",
    prerequisites=["quadratic"],
))

register_atom(Atom(
    atom_type="formula",
    name="catalan_application",
    content=(
        "Catalan numbers C_n = C(2n,n)/(n+1) = (2n)!/((n+1)!*n!) "
        "count many combinatorial objects: balanced parentheses, "
        "full binary trees with n+1 leaves, monotone lattice paths "
        "that don't cross the diagonal, triangulations of (n+2)-gon. "
        "Recurrence: C_0=1, C_{n+1} = sum_{i=0}^{n} C_i*C_{n-i}."
    ),
    example=(
        "C_4 = C(8,4)/5 = 70/5 = 14. "
        "There are 14 ways to parenthesise 5 factors, "
        "14 full binary trees with 5 leaves, "
        "14 monotone paths in a 4x4 grid below the diagonal."
    ),
    tier=6,
    domain="combinatorics",
    source="Wikipedia contributors, 'Catalan number', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Catalan_number",
    prerequisites=["binomial"],
))

register_atom(Atom(
    atom_type="theorem",
    name="double_counting",
    content=(
        "Double counting (bijective proof technique) proves an identity "
        "by counting the same set in two different ways. If set S can "
        "be counted as |S| = A by one method and |S| = B by another, "
        "then A = B. Classic example: handshaking lemma -- sum of "
        "degrees = 2 * number of edges."
    ),
    example=(
        "Handshaking lemma: graph with edges {(1,2),(2,3),(3,1),(3,4)}. "
        "Degrees: d(1)=2, d(2)=2, d(3)=3, d(4)=1. "
        "Sum of degrees = 8 = 2 * 4 edges"
    ),
    tier=4,
    domain="combinatorics",
    source="Wikipedia contributors, 'Double counting (proof technique)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Double_counting_(proof_technique)",
    prerequisites=["counting"],
))

register_atom(Atom(
    atom_type="theorem",
    name="pigeonhole_application",
    content=(
        "The pigeonhole principle states that if n items are placed "
        "into m containers with n > m, then at least one container "
        "has more than one item. Generalised: at least one container "
        "has ceil(n/m) items. Applications include proving existence "
        "of repeated remainders, birthday paradox bounds, and "
        "Ramsey-type results."
    ),
    example=(
        "Among 13 people, at least ceil(13/12) = 2 share a birth month. "
        "Among 5 integers, at least 2 have the same remainder mod 4 "
        "(since there are only 4 possible remainders: 0,1,2,3)."
    ),
    tier=4,
    domain="combinatorics",
    source="Wikipedia contributors, 'Pigeonhole principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pigeonhole_principle",
    prerequisites=["counting"],
))

register_atom(Atom(
    atom_type="formula",
    name="compositions",
    content=(
        "A composition of n into k parts is an ordered sequence "
        "(a1, a2, ..., ak) with a_i >= 1 and sum = n. The number "
        "of compositions of n into k parts is C(n-1, k-1) (stars "
        "and bars with ordering). The total number of compositions "
        "of n is 2^{n-1}."
    ),
    example=(
        "Compositions of 4 into 2 parts: C(3,1) = 3. "
        "They are: (1,3), (2,2), (3,1). "
        "Total compositions of 4: 2^3 = 8: "
        "(4), (1,3), (2,2), (3,1), (1,1,2), (1,2,1), (2,1,1), (1,1,1,1)"
    ),
    tier=4,
    domain="combinatorics",
    source="Wikipedia contributors, 'Composition (combinatorics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Composition_(combinatorics)",
    prerequisites=["binomial", "stars_and_bars"],
))
