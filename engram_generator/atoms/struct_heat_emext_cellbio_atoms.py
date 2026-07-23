"""Knowledge atoms for structural engineering, heat transfer, EM ext, and cell biology ext."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Structural engineering (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="beam_deflection",
    content=(
        "The maximum deflection of a simply supported beam with a "
        "concentrated load P at the center is: delta = P*L^3 / (48*E*I), "
        "where L is the span, E is Young's modulus, and I is the "
        "second moment of area. For a uniformly distributed load w: "
        "delta = 5*w*L^4 / (384*E*I)."
    ),
    example=(
        "P=10 kN, L=6 m, E=200 GPa, I=8000 cm^4: "
        "delta = 10e3*6^3 / (48*200e9*8e-5) = 2160e3 / 768e6 = 2.81 mm."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Deflection (engineering)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Deflection_(engineering)",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="truss_analysis",
    content=(
        "Truss analysis determines member forces using the method of "
        "joints or sections. At each joint, equilibrium requires "
        "sum F_x = 0, sum F_y = 0. Members carry only axial forces "
        "(tension or compression). Determinacy requires m + r = 2j, "
        "where m = members, r = reactions, j = joints."
    ),
    example=(
        "Simple truss: 3 members, 3 joints, 3 reactions. m+r=6, 2j=6: "
        "determinate. Joint A: F_AB*cos(60) = R_Ax, F_AB*sin(60) + R_Ay = P."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Truss', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Truss#Analysis",
    prerequisites=["system_equations"],
))

register_atom(Atom(
    atom_type="formula",
    name="buckling_load",
    content=(
        "Euler's critical buckling load for a slender column: "
        "P_cr = pi^2 * E * I / (K*L)^2, where E is Young's modulus, "
        "I is the minimum second moment of area, L is the unsupported "
        "length, and K is the effective length factor (K=1 for pinned-pinned, "
        "K=0.5 for fixed-fixed)."
    ),
    example=(
        "E=200 GPa, I=500 cm^4, L=3 m, K=1: "
        "P_cr = pi^2*200e9*5e-5 / 9 = 10.97 MN."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Euler's critical load', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euler%27s_critical_load",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="moment_of_inertia",
    content=(
        "The second moment of area (area moment of inertia) measures a "
        "cross-section's resistance to bending. For a rectangle: "
        "I = b*h^3/12. For a circle: I = pi*r^4/4. The parallel axis "
        "theorem: I = I_cm + A*d^2."
    ),
    example=(
        "Rectangle b=0.1 m, h=0.2 m: I = 0.1*0.2^3/12 = 6.667e-5 m^4."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Second moment of area', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Second_moment_of_area",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="shear_bending",
    content=(
        "For a beam under loading, the shear force V and bending moment "
        "M are related by: dM/dx = V and dV/dx = -w(x), where w is "
        "the distributed load. The bending stress: sigma = M*y/I, "
        "maximum at the extreme fibre."
    ),
    example=(
        "Cantilever beam, point load P=5 kN at tip, L=2 m: "
        "V = -P = -5 kN (constant). M = -P*x, max |M| = P*L = 10 kN-m at support."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Shear and moment diagram', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shear_and_moment_diagram",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="section_modulus",
    content=(
        "The elastic section modulus S = I/c, where I is the second "
        "moment of area and c is the distance from the neutral axis to "
        "the extreme fibre. The maximum bending stress: sigma_max = M/S. "
        "For a rectangle: S = b*h^2/6."
    ),
    example=(
        "Rectangle b=0.1 m, h=0.3 m: S = 0.1*0.3^2/6 = 1.5e-3 m^3. "
        "M=50 kN-m: sigma = 50e3/1.5e-3 = 33.3 MPa."
    ),
    tier=5,
    domain="structural_engineering",
    source="Wikipedia contributors, 'Section modulus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Section_modulus",
    prerequisites=["moment_of_inertia"],
))

# ---------------------------------------------------------------------------
# Heat transfer (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="law",
    name="fourier_conduction",
    content=(
        "Fourier's law of heat conduction states that the heat flux is "
        "proportional to the negative temperature gradient: "
        "q = -k * dT/dx, where k is thermal conductivity (W/m-K). "
        "For a plane wall of thickness L: Q = k*A*(T1-T2)/L."
    ),
    example=(
        "k=50 W/m-K, A=2 m^2, T1=100C, T2=20C, L=0.1 m: "
        "Q = 50*2*(100-20)/0.1 = 80,000 W = 80 kW."
    ),
    tier=4,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Thermal conduction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Thermal_conduction",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="law",
    name="newton_cooling",
    content=(
        "Newton's law of cooling states that the rate of convective "
        "heat transfer is proportional to the temperature difference: "
        "Q = h*A*(T_s - T_inf), where h is the convection coefficient "
        "(W/m^2-K), A is the surface area, T_s is surface temperature, "
        "and T_inf is fluid temperature."
    ),
    example=(
        "h=25 W/m^2-K, A=0.5 m^2, T_s=80C, T_inf=20C: "
        "Q = 25*0.5*(80-20) = 750 W."
    ),
    tier=4,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Newton's law of cooling', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Newton%27s_law_of_cooling",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="law",
    name="stefan_boltzmann",
    content=(
        "The Stefan-Boltzmann law gives the total radiative heat flux "
        "from a blackbody: q = sigma * T^4, where sigma = 5.67e-8 W/m^2-K^4. "
        "For a grey body with emissivity epsilon: q = epsilon*sigma*T^4. "
        "Net radiation between two surfaces involves view factors."
    ),
    example=(
        "T=500 K, epsilon=0.8, A=1 m^2: "
        "Q = 0.8*5.67e-8*500^4*1 = 0.8*5.67e-8*6.25e10 = 2835 W."
    ),
    tier=4,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Stefan-Boltzmann law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_law",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="heat_exchanger",
    content=(
        "The heat exchanger effectiveness-NTU method: epsilon = Q/Q_max, "
        "where Q_max = C_min*(T_h_in - T_c_in). NTU = UA/C_min. "
        "For a counter-flow exchanger: epsilon = (1-exp(-NTU*(1-C_r))) / "
        "(1-C_r*exp(-NTU*(1-C_r))), where C_r = C_min/C_max."
    ),
    example=(
        "C_min=1000 W/K, C_max=2000 W/K, UA=1500 W/K: "
        "NTU=1.5, C_r=0.5. epsilon=(1-exp(-0.75))/(1-0.5*exp(-0.75))=0.627."
    ),
    tier=5,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Heat exchanger', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Heat_exchanger#Analysis",
    prerequisites=["exponential_dist"],
))

register_atom(Atom(
    atom_type="formula",
    name="fin_efficiency",
    content=(
        "A fin enhances heat transfer by extending surface area. "
        "Fin efficiency: eta_f = tanh(m*L) / (m*L), where "
        "m = sqrt(h*P / (k*A_c)), h is convection coefficient, "
        "P is fin perimeter, k is conductivity, A_c is cross-section area."
    ),
    example=(
        "Rectangular fin: h=50, k=200, thickness=2mm, L=20mm. "
        "P=2*(w+t), A_c=w*t. m=sqrt(50*2.004/(200*0.001))=22.4. "
        "mL=22.4*0.02=0.448. eta=tanh(0.448)/0.448=0.94."
    ),
    tier=5,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Fin (extended surface)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fin_(extended_surface)",
    prerequisites=["fourier_conduction"],
))

register_atom(Atom(
    atom_type="formula",
    name="thermal_resistance",
    content=(
        "Thermal resistance is the temperature difference per unit heat "
        "flow: R = delta_T / Q. For conduction through a wall: "
        "R_cond = L / (k*A). For convection: R_conv = 1 / (h*A). "
        "Resistances in series add: R_total = R1 + R2 + ..."
    ),
    example=(
        "Wall: L=0.2m, k=1.5, A=10 m^2. R_cond=0.2/(1.5*10)=0.0133 K/W. "
        "Convection: h=25. R_conv=1/(25*10)=0.004 K/W. "
        "R_total = 0.0133+0.004 = 0.0173 K/W."
    ),
    tier=4,
    domain="heat_transfer",
    source="Wikipedia contributors, 'Thermal resistance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Thermal_resistance",
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Electromagnetism extensions (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="electric_dipole",
    content=(
        "An electric dipole moment p = q*d, where q is the charge and d "
        "is the separation. The electric field on the axis at distance r "
        ">> d: E = 2*k*p / r^3. Perpendicular to the axis: E = k*p / r^3. "
        "The potential: V = k*p*cos(theta) / r^2."
    ),
    example=(
        "q=1e-9 C, d=0.01 m: p=1e-11 C-m. At r=0.1 m on axis: "
        "E = 2*8.99e9*1e-11/0.001 = 0.1798 V/m."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Electric dipole moment', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Electric_dipole_moment",
    prerequisites=["coulombs_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="capacitor_energy",
    content=(
        "The energy stored in a capacitor: U = Q^2/(2C) = CV^2/2 = QV/2, "
        "where C is capacitance, V is voltage, Q is charge. "
        "For a parallel-plate capacitor: C = epsilon_0*A/d."
    ),
    example=(
        "C=10 uF, V=100 V: U = 0.5*10e-6*100^2 = 0.05 J = 50 mJ."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Capacitor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Capacitor#Energy_stored_in_a_capacitor",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="law",
    name="magnetic_field_wire",
    content=(
        "The magnetic field at distance r from an infinite straight "
        "current-carrying wire: B = mu_0*I / (2*pi*r), where "
        "mu_0 = 4*pi*1e-7 T-m/A. Direction given by the right-hand rule."
    ),
    example=(
        "I=10 A, r=0.05 m: B = 4*pi*1e-7*10/(2*pi*0.05) "
        "= 4e-5 T = 40 uT."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Biot-Savart law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Biot%E2%80%93Savart_law",
    prerequisites=["coulombs_law"],
))

register_atom(Atom(
    atom_type="law",
    name="ampere_law",
    content=(
        "Ampere's law (integral form): the line integral of B around "
        "a closed loop equals mu_0 times the enclosed current: "
        "oint B . dl = mu_0 * I_enc. For a solenoid with n turns per "
        "unit length: B = mu_0 * n * I inside."
    ),
    example=(
        "Solenoid: n=1000 turns/m, I=2 A: "
        "B = 4*pi*1e-7*1000*2 = 2.513e-3 T = 2.513 mT."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Ampere's circuital law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Amp%C3%A8re%27s_circuital_law",
    prerequisites=["magnetic_field_wire"],
))

register_atom(Atom(
    atom_type="law",
    name="displacement_current",
    content=(
        "Maxwell's addition to Ampere's law: the displacement current "
        "density J_d = epsilon_0 * dE/dt. The modified Ampere's law: "
        "curl B = mu_0*(J + epsilon_0*dE/dt). This completes Maxwell's "
        "equations and predicts electromagnetic waves."
    ),
    example=(
        "Parallel plate capacitor charging: dE/dt = I/(epsilon_0*A). "
        "I_d = epsilon_0*A*dE/dt = I. Displacement current equals "
        "conduction current."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'Displacement current', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Displacement_current",
    prerequisites=["ampere_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="lc_oscillation",
    content=(
        "An LC circuit oscillates at angular frequency omega = 1/sqrt(LC). "
        "The charge: q(t) = Q_0*cos(omega*t + phi). Current: "
        "i(t) = -Q_0*omega*sin(omega*t + phi). Energy oscillates between "
        "capacitor (U_C = q^2/2C) and inductor (U_L = Li^2/2)."
    ),
    example=(
        "L=0.1 H, C=100 uF: omega = 1/sqrt(0.1*1e-4) = 316.2 rad/s. "
        "f = 316.2/(2*pi) = 50.3 Hz. Period T = 19.9 ms."
    ),
    tier=5,
    domain="electromagnetism",
    source="Wikipedia contributors, 'LC circuit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/LC_circuit",
    prerequisites=["rc_circuit"],
))

# ---------------------------------------------------------------------------
# Cell biology extensions (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="concept",
    name="cell_signaling",
    content=(
        "Cell signalling involves ligand binding to receptors, triggering "
        "intracellular cascades. Key pathways: MAPK/ERK (growth), "
        "PI3K/Akt (survival), JAK/STAT (immune), Wnt (development). "
        "Signal amplification occurs through kinase cascades where each "
        "enzyme activates many downstream molecules."
    ),
    example=(
        "EGF binds EGFR -> Ras-GTP -> Raf -> MEK -> ERK. "
        "1 receptor activates ~10 Ras, each activates ~10 Raf, "
        "giving 100x amplification at the ERK level."
    ),
    tier=5,
    domain="cell_biology",
    source="Wikipedia contributors, 'Cell signaling', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cell_signaling",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="concept",
    name="gene_expression_regulation",
    content=(
        "Gene expression is regulated at multiple levels: transcriptional "
        "(promoters, enhancers, transcription factors), post-transcriptional "
        "(mRNA splicing, stability, miRNA), translational (initiation "
        "factors, ribosome availability), and post-translational "
        "(protein modification, degradation)."
    ),
    example=(
        "Lac operon: no lactose -> repressor binds operator -> no transcription. "
        "Lactose present -> allolactose binds repressor -> repressor released -> "
        "RNA polymerase transcribes lacZYA."
    ),
    tier=5,
    domain="cell_biology",
    source="Wikipedia contributors, 'Regulation of gene expression', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Regulation_of_gene_expression",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="concept",
    name="cell_cycle_checkpoint",
    content=(
        "Cell cycle checkpoints ensure proper progression: G1/S (DNA "
        "damage?), intra-S (replication errors?), G2/M (DNA fully "
        "replicated?), spindle assembly (chromosomes aligned?). "
        "p53 is a key G1/S checkpoint protein that halts the cycle or "
        "triggers apoptosis upon detecting DNA damage."
    ),
    example=(
        "UV damage -> ATR kinase -> Chk1 -> phosphorylates Cdc25 -> "
        "Cdc25 degraded -> CDK2 remains inactive -> G1/S arrest."
    ),
    tier=5,
    domain="cell_biology",
    source="Wikipedia contributors, 'Cell cycle checkpoint', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cell_cycle_checkpoint",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="pcr_amplification",
    content=(
        "Polymerase chain reaction amplifies DNA exponentially: "
        "N = N_0 * 2^n (ideal) or N = N_0 * (1+E)^n (with efficiency E). "
        "Each cycle doubles the target: denaturation (95C), annealing "
        "(50-65C), extension (72C). After 30 cycles: 2^30 ~ 10^9 copies."
    ),
    example=(
        "N_0 = 100 copies, n = 25 cycles, E = 0.9: "
        "N = 100 * 1.9^25 = 100 * 7.18e6 = 7.18e8 copies."
    ),
    tier=5,
    domain="cell_biology",
    source="Wikipedia contributors, 'Polymerase chain reaction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Polymerase_chain_reaction",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="concept",
    name="apoptosis_pathway",
    content=(
        "Apoptosis (programmed cell death) proceeds via intrinsic "
        "(mitochondrial) or extrinsic (death receptor) pathways. "
        "Intrinsic: stress -> Bax/Bak pores -> cytochrome c release -> "
        "apoptosome -> caspase-9 -> caspase-3. Extrinsic: Fas/TNF "
        "ligand -> FADD -> caspase-8 -> caspase-3."
    ),
    example=(
        "DNA damage -> p53 upregulates Bax -> Bax oligomerises in "
        "mitochondrial membrane -> cytochrome c released -> binds Apaf-1 "
        "-> activates caspase-9 -> activates caspase-3 -> cell death."
    ),
    tier=5,
    domain="cell_biology",
    source="Wikipedia contributors, 'Apoptosis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Apoptosis",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="receptor_binding",
    content=(
        "Receptor-ligand binding follows the law of mass action: "
        "[RL] = [R_total]*[L] / (K_d + [L]), where K_d is the "
        "dissociation constant. Fractional occupancy: "
        "theta = [L]/(K_d + [L]). At [L] = K_d, 50% of receptors "
        "are occupied."
    ),
    example=(
        "K_d = 10 nM, [L] = 30 nM: theta = 30/(10+30) = 0.75. "
        "75% of receptors are occupied."
    ),
    tier=5,
    domain="cell_biology",
    source="Wikipedia contributors, 'Receptor-ligand kinetics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Receptor%E2%80%93ligand_kinetics",
    prerequisites=["michaelis_menten"],
))
