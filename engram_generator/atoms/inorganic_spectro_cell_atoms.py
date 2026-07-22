"""Knowledge atoms for inorganic chemistry, spectroscopy, and cell biology.

Covers crystal field theory, coordination chemistry, spectroscopic
analysis techniques, and fundamental cell biology processes. Each atom
includes a worked example with concrete values for verification.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Inorganic Chemistry (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="crystal_field",
    content=(
        "Crystal field theory (CFT) describes the breaking of orbital "
        "degeneracy in transition metal complexes due to electrostatic "
        "interactions between the d-electrons and the ligand field. In an "
        "octahedral field, the five d-orbitals split into a lower t_2g set "
        "(d_xy, d_xz, d_yz) and an upper e_g set (d_z^2, d_x^2-y^2). The "
        "energy difference is called the crystal field splitting energy "
        "Delta_oct. The crystal field stabilisation energy (CFSE) is: "
        "CFSE = (-0.4 * n_t2g + 0.6 * n_eg) * Delta_oct, where n_t2g and "
        "n_eg are the number of electrons in the respective sets."
    ),
    example=(
        "Fe^2+ (d^6) in octahedral field (high spin): t_2g^4 e_g^2. "
        "CFSE = (-0.4*4 + 0.6*2) * Delta_oct = (-1.6 + 1.2) * Delta_oct "
        "= -0.4 * Delta_oct"
    ),
    tier=5,
    domain="inorganic_chemistry",
    source=(
        "Wikipedia contributors, 'Crystal field theory', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Crystal_field_theory",
    prerequisites=["electron_config"],
))

register_atom(Atom(
    atom_type="definition",
    name="coordination_number",
    content=(
        "The coordination number of a central atom in a coordination "
        "compound is the number of atoms, ions, or molecules (ligands) "
        "directly bonded to it. Common coordination numbers include 2 "
        "(linear), 4 (tetrahedral or square planar), 6 (octahedral), "
        "and 8 (square antiprismatic). The coordination number determines "
        "the geometry of the complex."
    ),
    example=(
        "[Cu(NH3)4]^2+: Cu^2+ is bonded to 4 NH3 ligands, "
        "coordination number = 4, geometry = square planar"
    ),
    tier=4,
    domain="inorganic_chemistry",
    source=(
        "Wikipedia contributors, 'Coordination number', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Coordination_number",
    prerequisites=["lewis_structure"],
))

register_atom(Atom(
    atom_type="definition",
    name="isomer_coordination",
    content=(
        "Coordination isomerism occurs in compounds containing complex "
        "cations and complex anions, where the distribution of ligands "
        "between the two metal centres differs. Geometric isomerism (cis "
        "and trans) occurs in square planar and octahedral complexes when "
        "identical ligands can occupy different positions relative to each "
        "other. Linkage isomerism occurs when an ambidentate ligand (e.g. "
        "NO2^- / ONO^-) coordinates through different atoms."
    ),
    example=(
        "[Co(NH3)4Cl2]+: cis isomer has both Cl adjacent (90 degrees), "
        "trans isomer has Cl opposite (180 degrees). Total geometric "
        "isomers = 2"
    ),
    tier=5,
    domain="inorganic_chemistry",
    source=(
        "Wikipedia contributors, 'Coordination compound', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Coordination_complex#Isomerism",
    prerequisites=["coordination_number"],
))

register_atom(Atom(
    atom_type="definition",
    name="spectrochemical",
    content=(
        "The spectrochemical series is an empirically determined ordering "
        "of ligands by the strength of the crystal field splitting they "
        "produce. From weak field to strong field: I^- < Br^- < S^2- < "
        "Cl^- < N3^- < F^- < OH^- < ox^2- < H2O < NCS^- < CH3CN < py "
        "< NH3 < en < bipy < phen < NO2^- < PPh3 < CN^- < CO < NO+. "
        "Weak field ligands produce small Delta and high-spin complexes, "
        "while strong field ligands produce large Delta and low-spin "
        "complexes."
    ),
    example=(
        "[Fe(H2O)6]^2+: H2O is a weak field ligand, so Fe^2+ (d^6) is "
        "high spin with 4 unpaired electrons. [Fe(CN)6]^4-: CN^- is a "
        "strong field ligand, so Fe^2+ is low spin with 0 unpaired electrons."
    ),
    tier=5,
    domain="inorganic_chemistry",
    source=(
        "Wikipedia contributors, 'Spectrochemical series', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Spectrochemical_series",
    prerequisites=["crystal_field"],
))

register_atom(Atom(
    atom_type="formula",
    name="magnetic_moment",
    content=(
        "The spin-only magnetic moment of a transition metal ion is "
        "mu = sqrt(n(n+2)) Bohr magnetons, where n is the number of "
        "unpaired electrons. This formula assumes orbital angular momentum "
        "is quenched (valid for first-row transition metals in octahedral "
        "fields). Measured magnetic moments close to the spin-only value "
        "indicate quenched orbital contribution; deviations suggest "
        "orbital contribution is significant."
    ),
    example=(
        "Fe^3+ (d^5, high spin): 5 unpaired electrons. "
        "mu = sqrt(5*(5+2)) = sqrt(35) = 5.92 BM"
    ),
    tier=5,
    domain="inorganic_chemistry",
    source=(
        "Wikipedia contributors, 'Magnetic moment', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Magnetic_moment",
    prerequisites=["crystal_field"],
))

register_atom(Atom(
    atom_type="formula",
    name="solubility_product",
    content=(
        "The solubility product constant K_sp is the equilibrium constant "
        "for the dissolution of a sparingly soluble ionic compound. For "
        "A_mB_n(s) <-> mA^n+(aq) + nB^m-(aq), K_sp = [A^n+]^m * [B^m-]^n. "
        "The molar solubility s can be found from K_sp by expressing ion "
        "concentrations in terms of s: [A^n+] = m*s and [B^m-] = n*s, "
        "so K_sp = (m*s)^m * (n*s)^n."
    ),
    example=(
        "PbCl2: K_sp = 1.7e-5. PbCl2 -> Pb^2+ + 2Cl^-. "
        "K_sp = s * (2s)^2 = 4s^3. s = (1.7e-5 / 4)^(1/3) "
        "= (4.25e-6)^0.333 = 0.0162 M"
    ),
    tier=5,
    domain="inorganic_chemistry",
    source=(
        "Wikipedia contributors, 'Solubility equilibrium', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Solubility_equilibrium",
    prerequisites=["equilibrium_constant"],
))


# ---------------------------------------------------------------------------
# Spectroscopy (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="beer_lambert",
    content=(
        "The Beer-Lambert law relates the attenuation of light to the "
        "properties of the material through which it travels: "
        "A = epsilon * l * c, where A is the absorbance (dimensionless), "
        "epsilon is the molar attenuation coefficient (L/(mol*cm)), l is "
        "the optical path length (cm), and c is the concentration of the "
        "absorbing species (mol/L). Transmittance T = I/I_0 = 10^(-A)."
    ),
    example=(
        "epsilon = 1500 L/(mol*cm), l = 1 cm, c = 0.002 mol/L: "
        "A = 1500 * 1 * 0.002 = 3.0. T = 10^(-3.0) = 0.001 (0.1%)"
    ),
    tier=5,
    domain="spectroscopy",
    source=(
        "Wikipedia contributors, 'Beer-Lambert law', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law",
    prerequisites=["concentration"],
))

register_atom(Atom(
    atom_type="formula",
    name="wavelength_energy",
    content=(
        "The energy of a photon is related to its wavelength by "
        "E = hc/lambda, where h is Planck's constant (6.626e-34 J*s), "
        "c is the speed of light (3.0e8 m/s), and lambda is the "
        "wavelength in metres. Equivalently, E = h*nu where nu is the "
        "frequency. For wavelength in nm: E(eV) = 1240 / lambda(nm)."
    ),
    example=(
        "lambda = 500 nm (green light): E = 1240/500 = 2.48 eV. "
        "Or: E = (6.626e-34 * 3.0e8) / (500e-9) = 3.976e-19 J"
    ),
    tier=5,
    domain="spectroscopy",
    source=(
        "Wikipedia contributors, 'Photon energy', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Photon_energy",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="rule",
    name="nmr_splitting",
    content=(
        "In proton NMR spectroscopy, the (n+1) rule predicts the "
        "multiplicity of a signal: a proton with n equivalent neighbouring "
        "protons splits into (n+1) peaks. A singlet (s) has 0 neighbours, "
        "doublet (d) has 1, triplet (t) has 2, quartet (q) has 3, etc. "
        "The relative intensities follow Pascal's triangle (binomial "
        "coefficients). The coupling constant J (in Hz) measures the "
        "distance between peaks in a multiplet."
    ),
    example=(
        "Ethanol CH3CH2OH: CH3 has 2 neighbours (CH2), splits into "
        "triplet (t). CH2 has 3 neighbours (CH3), splits into quartet (q). "
        "OH is a singlet (rapid exchange)."
    ),
    tier=5,
    domain="spectroscopy",
    source=(
        "Wikipedia contributors, 'Proton nuclear magnetic resonance', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Proton_nuclear_magnetic_resonance",
    prerequisites=["organic_chemistry"],
))

register_atom(Atom(
    atom_type="rule",
    name="mass_spec_fragment",
    content=(
        "In mass spectrometry, the molecular ion (M+) peak appears at "
        "the molecular weight of the compound. Fragmentation produces "
        "smaller ions whose m/z values indicate structural features. "
        "Common losses: 15 (CH3), 17 (OH), 18 (H2O), 28 (CO or C2H4), "
        "29 (CHO), 31 (OCH3), 45 (OC2H5). The base peak is the most "
        "intense peak (100% relative intensity)."
    ),
    example=(
        "Butanone (CH3COCH2CH3, MW=72): M+ at m/z=72. Loss of CH3 "
        "(15) gives m/z=57. Loss of C2H5 (29) gives m/z=43 (base peak, "
        "CH3CO+)."
    ),
    tier=5,
    domain="spectroscopy",
    source=(
        "Wikipedia contributors, 'Mass spectrometry', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Mass_spectrometry",
    prerequisites=["molecular_weight"],
))

register_atom(Atom(
    atom_type="rule",
    name="ir_functional_group",
    content=(
        "Infrared spectroscopy identifies functional groups by their "
        "characteristic absorption frequencies. Key absorptions: O-H "
        "stretch 3200-3600 cm^-1 (broad), N-H stretch 3300-3500 cm^-1, "
        "C-H stretch 2850-3000 cm^-1, C=O stretch 1650-1750 cm^-1 "
        "(strong, sharp), C=C stretch 1600-1680 cm^-1, C-O stretch "
        "1000-1300 cm^-1. The fingerprint region (below 1500 cm^-1) is "
        "unique to each molecule."
    ),
    example=(
        "Acetic acid (CH3COOH): broad O-H at ~3000 cm^-1, strong C=O "
        "at ~1710 cm^-1, C-O at ~1290 cm^-1. These three peaks together "
        "identify a carboxylic acid."
    ),
    tier=5,
    domain="spectroscopy",
    source=(
        "Wikipedia contributors, 'Infrared spectroscopy', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Infrared_spectroscopy",
    prerequisites=["functional_group_id"],
))

register_atom(Atom(
    atom_type="formula",
    name="emission_spectrum",
    content=(
        "The Rydberg formula gives the wavelengths of spectral lines in "
        "the hydrogen emission spectrum: 1/lambda = R_H * (1/n1^2 - 1/n2^2), "
        "where R_H = 1.097e7 m^-1 is the Rydberg constant, n1 < n2 are "
        "principal quantum numbers. Named series: Lyman (n1=1, UV), "
        "Balmer (n1=2, visible), Paschen (n1=3, IR), Brackett (n1=4), "
        "Pfund (n1=5)."
    ),
    example=(
        "H-alpha line (Balmer series, n1=2, n2=3): "
        "1/lambda = 1.097e7 * (1/4 - 1/9) = 1.097e7 * 5/36 "
        "= 1.524e6 m^-1. lambda = 656.3 nm (red)"
    ),
    tier=5,
    domain="spectroscopy",
    source=(
        "Wikipedia contributors, 'Rydberg formula', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Rydberg_formula",
    prerequisites=["wavelength_energy"],
))


# ---------------------------------------------------------------------------
# Cell Biology (tier 3-4)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="mitosis_phase",
    content=(
        "Mitosis is the process of nuclear division in eukaryotic cells, "
        "producing two genetically identical daughter nuclei. The phases "
        "are: Prophase (chromatin condenses, nuclear envelope begins to "
        "break down), Metaphase (chromosomes align at the metaphase plate), "
        "Anaphase (sister chromatids separate and move to opposite poles), "
        "Telophase (nuclear envelopes reform, chromosomes decondense). "
        "Cytokinesis (cell division) typically follows telophase."
    ),
    example=(
        "Chromosomes aligned at cell equator, maximally condensed = "
        "Metaphase. Sister chromatids separating toward poles = Anaphase."
    ),
    tier=3,
    domain="cell_biology",
    source=(
        "Wikipedia contributors, 'Mitosis', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Mitosis",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="meiosis_gametes",
    content=(
        "Meiosis produces haploid gametes from diploid cells through two "
        "successive divisions (meiosis I and II). A diploid organism with "
        "2n chromosomes produces gametes with n chromosomes. The number of "
        "genetically unique gametes from independent assortment alone is "
        "2^n, where n is the haploid number. Crossing over further "
        "increases diversity. For humans (n=23): 2^23 = 8,388,608 "
        "possible gamete combinations from assortment alone."
    ),
    example=(
        "Organism with 2n=6 (n=3): number of unique gametes from "
        "independent assortment = 2^3 = 8. After meiosis, each gamete "
        "has 3 chromosomes."
    ),
    tier=4,
    domain="cell_biology",
    source=(
        "Wikipedia contributors, 'Meiosis', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Meiosis",
    prerequisites=["mitosis_phase"],
))

register_atom(Atom(
    atom_type="definition",
    name="membrane_transport",
    content=(
        "Membrane transport moves substances across the cell membrane. "
        "Passive transport requires no energy: simple diffusion (small "
        "nonpolar molecules), facilitated diffusion (channels/carriers), "
        "and osmosis (water through aquaporins). Active transport requires "
        "ATP: primary active transport (Na+/K+ ATPase pumps 3 Na+ out "
        "and 2 K+ in per ATP), secondary active transport (symport/ "
        "antiport driven by ion gradient). Endocytosis and exocytosis "
        "transport large molecules via vesicles."
    ),
    example=(
        "Na+/K+ ATPase: 1 ATP hydrolysed, 3 Na+ pumped out, 2 K+ "
        "pumped in. Net charge change per cycle = +1 (electrogenic). "
        "This is primary active transport."
    ),
    tier=3,
    domain="cell_biology",
    source=(
        "Wikipedia contributors, 'Membrane transport', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Membrane_transport",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="atp_yield",
    content=(
        "Complete oxidation of one glucose molecule through aerobic "
        "respiration yields approximately 30-32 ATP. The breakdown: "
        "Glycolysis produces 2 ATP (substrate-level) + 2 NADH. "
        "Pyruvate decarboxylation produces 2 NADH. The citric acid "
        "cycle produces 2 ATP (GTP) + 6 NADH + 2 FADH2. Oxidative "
        "phosphorylation: each NADH yields ~2.5 ATP, each FADH2 "
        "yields ~1.5 ATP. Total: 2 + 2 + 10*2.5 + 2*1.5 = 30-32 ATP."
    ),
    example=(
        "1 glucose: glycolysis 2 ATP + 2 NADH(5 ATP), pyruvate "
        "decarboxylation 2 NADH(5 ATP), TCA 2 GTP + 6 NADH(15 ATP) + "
        "2 FADH2(3 ATP). Total = 2 + 5 + 5 + 2 + 15 + 3 = 32 ATP"
    ),
    tier=4,
    domain="cell_biology",
    source=(
        "Wikipedia contributors, 'Oxidative phosphorylation', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Oxidative_phosphorylation",
    prerequisites=["membrane_transport"],
))

register_atom(Atom(
    atom_type="formula",
    name="cell_cycle_duration",
    content=(
        "The eukaryotic cell cycle consists of interphase (G1, S, G2) "
        "and mitotic (M) phase. G1 is the first gap phase (cell growth), "
        "S phase is DNA synthesis (chromosome replication), G2 is the "
        "second gap phase (preparation for mitosis), M is mitosis. "
        "Typical mammalian cell cycle: G1 ~10h, S ~8h, G2 ~4h, M ~1h, "
        "total ~23h. The fraction of cells in a given phase approximates "
        "the fraction of time spent in that phase."
    ),
    example=(
        "Cell cycle 24h total. G1=11h, S=8h, G2=4h, M=1h. "
        "Fraction in S phase = 8/24 = 0.333. In a population of "
        "1000 cells, ~333 are in S phase."
    ),
    tier=4,
    domain="cell_biology",
    source=(
        "Wikipedia contributors, 'Cell cycle', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Cell_cycle",
    prerequisites=["mitosis_phase"],
))

register_atom(Atom(
    atom_type="formula",
    name="osmolarity",
    content=(
        "Osmolarity is the concentration of osmotically active particles "
        "in a solution, measured in osmoles per litre (Osm/L). For an "
        "ionic compound, osmolarity = molarity * n * i, where n is the "
        "number of particles the compound dissociates into (van't Hoff "
        "factor i for strong electrolytes equals n). For NaCl, i=2 "
        "(Na+ + Cl-). Isotonic solutions have osmolarity ~300 mOsm/L. "
        "Cells in hypertonic solution shrink (crenation); in hypotonic "
        "solution they swell (lysis)."
    ),
    example=(
        "0.15 M NaCl (i=2): osmolarity = 0.15 * 2 = 0.3 Osm/L = "
        "300 mOsm/L (isotonic with blood). 0.3 M glucose (i=1): "
        "osmolarity = 0.3 * 1 = 0.3 Osm/L = 300 mOsm/L (also isotonic)."
    ),
    tier=4,
    domain="cell_biology",
    source=(
        "Wikipedia contributors, 'Osmotic concentration', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Osmotic_concentration",
    prerequisites=["molarity"],
))
