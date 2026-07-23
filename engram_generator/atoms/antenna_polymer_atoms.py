"""Knowledge atoms for antenna theory and polymer science."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ---------------------------------------------------------------------------
# Antenna Theory (tiers 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="antenna_directivity",
    content="Directivity D is the ratio of maximum radiation intensity to the average: D = U_max / U_avg = 4*pi*U_max / P_rad. For a short dipole: D = 1.5 (1.76 dBi). For a half-wave dipole: D = 1.64 (2.15 dBi). Isotropic antenna: D = 1.",
    example="Half-wave dipole: P_rad=1W, U_max = D*P_rad/(4*pi) = 1.64/(4*pi) = 0.1305 W/sr.",
    tier=5, domain="antenna_theory",
    source="Wikipedia contributors, 'Directivity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Directivity",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="antenna_gain_efficiency",
    content="Antenna gain G = eta * D, where eta is radiation efficiency (0-1) and D is directivity. G accounts for ohmic losses. In dBi: G_dBi = 10*log10(G). The effective isotropic radiated power: EIRP = P_t * G.",
    example="D=6 (7.78 dBi), eta=0.8: G = 0.8*6 = 4.8 (6.81 dBi). With P_t=10W: EIRP = 48W.",
    tier=5, domain="antenna_theory",
    source="Wikipedia contributors, 'Antenna gain', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Antenna_gain",
    prerequisites=["antenna_directivity"],
))

register_atom(Atom(
    atom_type="formula",
    name="friis_transmission",
    content="The Friis transmission equation gives received power: P_r = P_t*G_t*G_r*(lambda/(4*pi*d))^2, where P_t is transmitted power, G_t, G_r are antenna gains, lambda is wavelength, d is distance. In dB: P_r(dB) = P_t(dB) + G_t(dB) + G_r(dB) - 20*log10(4*pi*d/lambda).",
    example="P_t=1W, G_t=G_r=10(=10dBi), f=2.4GHz(lambda=0.125m), d=100m: FSPL = (4*pi*100/0.125)^2 = (10053)^2 = 1.01e8 = 80dB. P_r = 0+10+10-80 = -60dBm = 1nW.",
    tier=5, domain="antenna_theory",
    source="Wikipedia contributors, 'Friis transmission equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Friis_transmission_equation",
    prerequisites=["antenna_gain_efficiency"],
))

register_atom(Atom(
    atom_type="formula",
    name="dipole_radiation",
    content="A short (Hertzian) dipole of length dL carrying current I radiates power P = (eta_0*k^2*I^2*dL^2)/(12*pi), where k=2*pi/lambda, eta_0=377 ohms. The radiation pattern is sin^2(theta) (donut shape). Radiation resistance: R_rad = 80*pi^2*(dL/lambda)^2.",
    example="dL=0.1*lambda, I=1A: R_rad = 80*pi^2*0.01 = 7.9 ohms. P = 0.5*1^2*7.9 = 3.95W.",
    tier=5, domain="antenna_theory",
    source="Wikipedia contributors, 'Dipole antenna', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dipole_antenna",
    prerequisites=["electromagnetic_wave"],
))

register_atom(Atom(
    atom_type="formula",
    name="array_factor",
    content="The array factor for N uniformly spaced elements: AF = sin(N*psi/2)/(N*sin(psi/2)), where psi = k*d*cos(theta) + beta, d is spacing, beta is progressive phase shift. The pattern is the product of element pattern and array factor. Main beam steers to theta_0 where psi=0: beta = -k*d*cos(theta_0).",
    example="N=4, d=lambda/2, beta=0: AF peaks at theta=90 (broadside). Nulls at psi=2*pi*n/N. First null at cos(theta)=lambda/(N*d)=0.5, theta=60 degrees.",
    tier=6, domain="antenna_theory",
    source="Wikipedia contributors, 'Phased array', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Phased_array",
    prerequisites=["friis_transmission"],
))

register_atom(Atom(
    atom_type="formula",
    name="effective_aperture",
    content="The effective aperture A_e relates antenna gain to physical area: A_e = G*lambda^2/(4*pi). For a parabolic dish: A_e = eta_a*pi*(D/2)^2, where eta_a is aperture efficiency (typically 0.55-0.7). Received power: P_r = S*A_e, where S is power flux density (W/m^2).",
    example="G=30dBi=1000, f=10GHz(lambda=0.03m): A_e = 1000*0.03^2/(4*pi) = 0.9/12.57 = 0.0716 m^2. Equivalent dish D = sqrt(4*A_e/(0.6*pi)) = 0.39m.",
    tier=6, domain="antenna_theory",
    source="Wikipedia contributors, 'Antenna aperture', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Antenna_aperture",
    prerequisites=["antenna_gain_efficiency"],
))

# ---------------------------------------------------------------------------
# Polymer Science (tiers 4-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="degree_polymerisation",
    content="The degree of polymerisation (DP) is the number of repeat units in a polymer chain: DP = M_n / M_0, where M_n is number-average molecular weight and M_0 is the monomer molecular weight. For condensation polymers: DP = 1/(1-p), where p is the extent of reaction (Carothers equation).",
    example="Nylon-6,6: M_0=226 g/mol, M_n=22600 g/mol. DP = 22600/226 = 100 repeat units.",
    tier=4, domain="polymer_science",
    source="Wikipedia contributors, 'Degree of polymerization', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Degree_of_polymerization",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="molecular_weight_avg",
    content="Number-average: M_n = sum(N_i*M_i)/sum(N_i). Weight-average: M_w = sum(N_i*M_i^2)/sum(N_i*M_i). Polydispersity index PDI = M_w/M_n >= 1 (=1 for monodisperse). For step-growth: M_w/M_n = 1+p. For living polymerisation: PDI approaches 1.",
    example="Two fractions: N1=100 chains of M=10000, N2=50 chains of M=50000. M_n = (100*10000+50*50000)/150 = 3500000/150 = 23333. M_w = (100*1e8+50*2.5e9)/(100*10000+50*50000) = 1.35e11/3.5e6 = 38571. PDI=1.65.",
    tier=4, domain="polymer_science",
    source="Wikipedia contributors, 'Molar mass distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Molar_mass_distribution",
    prerequisites=["arithmetic_mean"],
))

register_atom(Atom(
    atom_type="formula",
    name="glass_transition",
    content="The glass transition temperature T_g is where an amorphous polymer transitions from glassy to rubbery. The Fox equation for copolymers: 1/T_g = w_1/T_g1 + w_2/T_g2. T_g increases with stiffness (aromatic backbone), polarity, and crosslinking. Below T_g: brittle. Above: flexible.",
    example="Copolymer: 60% PS (T_g=373K), 40% PB (T_g=218K). 1/T_g = 0.6/373 + 0.4/218 = 0.001609 + 0.001835 = 0.003444. T_g = 290K = 17C.",
    tier=5, domain="polymer_science",
    source="Wikipedia contributors, 'Glass transition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Glass_transition",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="end_to_end_distance",
    content="The root-mean-square end-to-end distance of a freely jointed chain: <r^2>^{1/2} = l*sqrt(N), where l is bond length and N is number of bonds. For a real chain with characteristic ratio C_inf: <r^2> = C_inf*N*l^2. Typical C_inf: PE=6.7, PS=10.",
    example="Polyethylene: l=0.154 nm, N=1000, C_inf=6.7. <r^2>^{1/2} = 0.154*sqrt(6.7*1000) = 0.154*81.85 = 12.6 nm.",
    tier=5, domain="polymer_science",
    source="Wikipedia contributors, 'Ideal chain', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ideal_chain",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="viscosity_intrinsic",
    content="Intrinsic viscosity [eta] relates to molecular weight via the Mark-Houwink equation: [eta] = K * M^a, where K and a are polymer-solvent specific constants. a = 0.5 for theta solvent (ideal), 0.6-0.8 for good solvents. Measured by extrapolating (eta_sp/c) to c=0.",
    example="Polystyrene in toluene: K=1.1e-4 dL/g, a=0.725. M=100000: [eta] = 1.1e-4 * 100000^0.725 = 1.1e-4 * 5623 = 0.619 dL/g.",
    tier=5, domain="polymer_science",
    source="Wikipedia contributors, 'Intrinsic viscosity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Intrinsic_viscosity",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="flory_huggins",
    content="Flory-Huggins theory describes polymer solution thermodynamics: Delta G_mix/(nkT) = phi_1*ln(phi_1) + (phi_2/N)*ln(phi_2) + chi*phi_1*phi_2, where phi_1 is solvent fraction, phi_2 is polymer fraction, N is degree of polymerisation, chi is the interaction parameter. Phase separation occurs when chi > chi_c = (1+1/sqrt(N))^2/2.",
    example="N=100, chi=0.6: chi_c = (1+0.1)^2/2 = 0.605. Since chi < chi_c (barely), the mixture is miscible.",
    tier=6, domain="polymer_science",
    source="Wikipedia contributors, 'Flory-Huggins solution theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Flory%E2%80%93Huggins_solution_theory",
    prerequisites=["logarithm"],
))
