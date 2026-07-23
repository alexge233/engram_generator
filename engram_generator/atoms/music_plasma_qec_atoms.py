"""Knowledge atoms for music theory, plasma physics, and quantum error correction."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ---------------------------------------------------------------------------
# Music Theory (tiers 3-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="interval_identify",
    content=(
        "A musical interval is the distance between two pitches, measured "
        "in semitones. Common intervals: unison (0), minor 2nd (1), "
        "major 2nd (2), minor 3rd (3), major 3rd (4), perfect 4th (5), "
        "tritone (6), perfect 5th (7), minor 6th (8), major 6th (9), "
        "minor 7th (10), major 7th (11), octave (12)."
    ),
    example="C to E = 4 semitones = major 3rd. C to G = 7 semitones = perfect 5th.",
    tier=3,
    domain="music_theory",
    source="Wikipedia contributors, 'Interval (music)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Interval_(music)",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="chord_construct",
    content=(
        "A chord is constructed by stacking intervals above a root note. "
        "Major triad: root + major 3rd (4 semitones) + perfect 5th (7). "
        "Minor triad: root + minor 3rd (3) + perfect 5th (7). "
        "Dominant 7th: root + 4 + 7 + 10 semitones. "
        "Diminished: root + 3 + 6 semitones."
    ),
    example="C major: C(0) + E(4) + G(7). A minor: A(0) + C(3) + E(7).",
    tier=4,
    domain="music_theory",
    source="Wikipedia contributors, 'Chord (music)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chord_(music)",
    prerequisites=["interval_identify"],
))

register_atom(Atom(
    atom_type="definition",
    name="chord_progression",
    content=(
        "A chord progression is a sequence of chords following harmonic "
        "rules. In Roman numeral analysis, I=tonic, IV=subdominant, "
        "V=dominant. Common progressions: I-IV-V-I (basic), "
        "I-V-vi-IV (pop), ii-V-I (jazz). Voice leading governs smooth "
        "transitions between chords."
    ),
    example="Key of C major: I-IV-V-I = C-F-G-C. I-V-vi-IV = C-G-Am-F.",
    tier=4,
    domain="music_theory",
    source="Wikipedia contributors, 'Chord progression', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chord_progression",
    prerequisites=["chord_construct"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="voice_leading",
    content=(
        "Voice leading describes how individual voices (parts) move from "
        "one chord to the next. Rules: prefer stepwise motion (2nds), "
        "avoid parallel 5ths and octaves, resolve leading tones upward, "
        "keep common tones when possible, move other voices by smallest "
        "interval."
    ),
    example=(
        "C major to G major (SATB): Bass C->G (5th), Tenor E->D (step down), "
        "Alto G->G (common tone), Soprano C->B (step down)."
    ),
    tier=5,
    domain="music_theory",
    source="Wikipedia contributors, 'Voice leading', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Voice_leading",
    prerequisites=["chord_progression"],
))

register_atom(Atom(
    atom_type="formula",
    name="frequency_ratio",
    content=(
        "In equal temperament, the frequency ratio between adjacent "
        "semitones is 2^(1/12) = 1.05946. The frequency of a note n "
        "semitones above A4 (440 Hz) is f = 440 * 2^(n/12). An octave "
        "doubles the frequency. A perfect fifth is 2^(7/12) = 1.4983."
    ),
    example=(
        "Middle C (C4) is 3 semitones below A4: "
        "f = 440 * 2^(-9/12) = 440 * 0.5946 = 261.63 Hz."
    ),
    tier=3,
    domain="music_theory",
    source="Wikipedia contributors, 'Equal temperament', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Equal_temperament",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="definition",
    name="rhythm_subdivision",
    content=(
        "Rhythm subdivision divides a beat into smaller equal parts. "
        "A whole note = 4 beats, half = 2, quarter = 1, eighth = 1/2, "
        "sixteenth = 1/4. Triplets divide a beat into 3 equal parts. "
        "Dotted notes add half their value: dotted quarter = 1.5 beats."
    ),
    example=(
        "4/4 time, quarter = 1 beat: 2 eighth notes = 1 beat. "
        "Triplet eighths: 3 notes in 1 beat, each = 1/3 beat. "
        "Dotted half = 3 beats."
    ),
    tier=3,
    domain="music_theory",
    source="Wikipedia contributors, 'Subdivision (music)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tuplet",
    prerequisites=[],
))

# ---------------------------------------------------------------------------
# Plasma Physics (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="debye_length",
    content=(
        "The Debye length is the scale over which mobile charges screen "
        "electric fields in a plasma: lambda_D = sqrt(epsilon_0 * k_B * T_e "
        "/ (n_e * e^2)), where T_e is electron temperature, n_e is "
        "electron density, e is electron charge. It is the fundamental "
        "length scale in plasma physics."
    ),
    example=(
        "T_e = 10 eV = 1.16e5 K, n_e = 1e18 m^-3: "
        "lambda_D = sqrt(8.854e-12 * 1.38e-23 * 1.16e5 / (1e18 * (1.6e-19)^2)) "
        "= sqrt(1.427e-29 / 2.56e-20) = sqrt(5.57e-10) = 2.36e-5 m."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Debye length', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Debye_length",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="plasma_frequency",
    content=(
        "The plasma frequency is the natural oscillation frequency of "
        "electrons in a plasma: omega_p = sqrt(n_e * e^2 / (m_e * epsilon_0)), "
        "where n_e is electron density, e is electron charge, m_e is "
        "electron mass. EM waves below this frequency cannot propagate."
    ),
    example=(
        "n_e = 1e18 m^-3: omega_p = sqrt(1e18 * (1.6e-19)^2 / "
        "(9.109e-31 * 8.854e-12)) = sqrt(2.56e-20 / 8.067e-42) "
        "= sqrt(3.17e21) = 5.63e10 rad/s. f_p = 8.97 GHz."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Plasma oscillation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Plasma_oscillation",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="cyclotron_frequency",
    content=(
        "The cyclotron frequency is the angular frequency at which a "
        "charged particle orbits in a uniform magnetic field: "
        "omega_c = |q|*B / m, where q is charge, B is magnetic field "
        "strength, m is particle mass. The cyclotron radius (Larmor radius) "
        "is r_L = v_perp / omega_c."
    ),
    example=(
        "Proton (q=1.6e-19 C, m=1.67e-27 kg) in B=1 T: "
        "omega_c = 1.6e-19 / 1.67e-27 = 9.58e7 rad/s. "
        "f_c = 15.24 MHz."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Cyclotron resonance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cyclotron_resonance",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="plasma_beta",
    content=(
        "Plasma beta is the ratio of thermal pressure to magnetic pressure: "
        "beta = n*k_B*T / (B^2 / (2*mu_0)), where n is particle density, "
        "T is temperature, B is magnetic field, mu_0 = 4*pi*1e-7 H/m. "
        "beta < 1: magnetically dominated. beta > 1: pressure dominated."
    ),
    example=(
        "n=1e20 m^-3, T=1e7 K, B=1 T: "
        "P_thermal = 1e20 * 1.38e-23 * 1e7 = 1.38e4 Pa. "
        "P_magnetic = 1^2 / (2*4*pi*1e-7) = 3.98e5 Pa. "
        "beta = 1.38e4 / 3.98e5 = 0.0347."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Beta (plasma physics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Beta_(plasma_physics)",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="coulomb_logarithm",
    content=(
        "The Coulomb logarithm ln(Lambda) characterises the ratio of "
        "maximum to minimum impact parameters in a plasma: "
        "ln(Lambda) = ln(lambda_D / b_min), where lambda_D is the Debye "
        "length and b_min is the distance of closest approach. Typical "
        "values range from 10-20 in laboratory plasmas."
    ),
    example=(
        "lambda_D = 2.36e-5 m, b_min = e^2/(4*pi*epsilon_0*k_B*T) "
        "= 1.44e-9 / (1.16e5 * 1.38e-23) = 8.99e-13 m. "
        "ln(Lambda) = ln(2.36e-5 / 8.99e-13) = ln(2.63e7) = 17.1."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Coulomb logarithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coulomb_logarithm",
    prerequisites=["debye_length", "logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="mhd_alfven",
    content=(
        "The Alfven speed is the characteristic velocity of magnetic "
        "disturbances in a magnetised plasma: v_A = B / sqrt(mu_0 * rho), "
        "where B is the magnetic field strength, mu_0 is the permeability "
        "of free space, and rho is the mass density. Alfven waves propagate "
        "along magnetic field lines at this speed."
    ),
    example=(
        "B = 0.1 T, rho = 1e-12 kg/m^3 (solar corona): "
        "v_A = 0.1 / sqrt(4*pi*1e-7 * 1e-12) = 0.1 / sqrt(1.257e-18) "
        "= 0.1 / 1.12e-9 = 8.93e7 m/s."
    ),
    tier=5,
    domain="plasma_physics",
    source="Wikipedia contributors, 'Alfven wave', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Alfv%C3%A9n_wave",
    prerequisites=["square_root"],
))

# ---------------------------------------------------------------------------
# Quantum Error Correction (tiers 6-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="bit_flip_code",
    content=(
        "The 3-qubit bit-flip code protects against X (bit-flip) errors "
        "by encoding |0> -> |000> and |1> -> |111>. A single bit-flip on "
        "any qubit is detected by measuring two syndrome bits (parities "
        "of adjacent pairs). The syndrome uniquely identifies the error "
        "location, allowing correction."
    ),
    example=(
        "Encode |1> -> |111>. Error on qubit 2: |111> -> |101>. "
        "Syndrome: Z1Z2 = (-1), Z2Z3 = (-1) -> error on qubit 2. "
        "Apply X on qubit 2: |101> -> |111>. Corrected."
    ),
    tier=6,
    domain="quantum_error_correction",
    source="Wikipedia contributors, 'Quantum error correction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantum_error_correction",
    prerequisites=["qubit_measure"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="phase_flip_code",
    content=(
        "The 3-qubit phase-flip code protects against Z (phase-flip) "
        "errors by encoding in the Hadamard basis: |0> -> |+++>, "
        "|1> -> |--->. A single Z error on any qubit is detected in "
        "the X basis. The code corrects by conjugating the bit-flip "
        "code with Hadamard gates."
    ),
    example=(
        "Encode |0> -> |+++>. Phase flip on qubit 1: |+++> -> |-++>. "
        "Apply H to all: |-++> -> |100>. Detect with bit-flip syndromes: "
        "error on qubit 1. Apply X, then H back."
    ),
    tier=6,
    domain="quantum_error_correction",
    source="Wikipedia contributors, 'Quantum error correction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantum_error_correction",
    prerequisites=["bit_flip_code"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="shor_code",
    content=(
        "Shor's 9-qubit code is the first quantum error-correcting code, "
        "protecting against arbitrary single-qubit errors. It concatenates "
        "the phase-flip code with the bit-flip code: each logical qubit "
        "is encoded into 3 blocks of 3 physical qubits. |0> -> "
        "(|000> + |111>)^3 / 2*sqrt(2)."
    ),
    example=(
        "Encode |0>: each of 3 groups stores (|000> + |111>)/sqrt(2). "
        "X error on qubit 5 (middle of group 2): detected by bit-flip "
        "syndromes within group 2. Z error detected by phase-flip "
        "syndromes across groups."
    ),
    tier=7,
    domain="quantum_error_correction",
    source="Wikipedia contributors, 'Shor's code (quantum)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantum_error_correction#Shor_code",
    prerequisites=["bit_flip_code", "phase_flip_code"],
))

register_atom(Atom(
    atom_type="definition",
    name="stabilizer_check",
    content=(
        "In the stabilizer formalism, a quantum error-correcting code is "
        "defined by a set of commuting Pauli operators (stabilizers) whose "
        "+1 eigenspace is the code space. Errors are detected by measuring "
        "each stabilizer generator: a -1 outcome indicates an error. The "
        "syndrome pattern identifies the error."
    ),
    example=(
        "[[5,1,3]] code has 4 stabilizer generators. Measuring all gives "
        "syndrome (1,-1,1,1) -> single X error on qubit 3. Apply X_3 "
        "to correct."
    ),
    tier=7,
    domain="quantum_error_correction",
    source="Wikipedia contributors, 'Stabilizer code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stabilizer_code",
    prerequisites=["shor_code"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="steane_code",
    content=(
        "The Steane code [[7,1,3]] is a CSS code based on the classical "
        "[7,4,3] Hamming code. It encodes 1 logical qubit into 7 physical "
        "qubits and corrects any single-qubit error. The X and Z stabilizers "
        "are derived from the Hamming parity-check matrix H. Syndromes "
        "are computed separately for X and Z errors."
    ),
    example=(
        "Logical |0> = sum of all even-weight codewords of Hamming [7,4]. "
        "Z error on qubit 3: Z syndrome from H gives binary 011 = qubit 3. "
        "Apply Z_3 to correct."
    ),
    tier=7,
    domain="quantum_error_correction",
    source="Wikipedia contributors, 'Steane code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Steane_code",
    prerequisites=["stabilizer_check"],
))

register_atom(Atom(
    atom_type="definition",
    name="logical_operators",
    content=(
        "Logical operators in a stabilizer code are Pauli operators that "
        "commute with all stabilizers but are not themselves stabilizers. "
        "They act on the encoded (logical) qubits. For an [[n,k,d]] code, "
        "there are 2k logical operators (k pairs of X_L, Z_L). The code "
        "distance d is the minimum weight of any logical operator."
    ),
    example=(
        "Steane [[7,1,3]]: logical X_L = X_1 X_2 X_3 X_4 X_5 X_6 X_7. "
        "Logical Z_L = Z_1 Z_2 Z_3 Z_4 Z_5 Z_6 Z_7. Both have weight 7 "
        "but equivalent operators of weight 3 exist, giving d=3."
    ),
    tier=7,
    domain="quantum_error_correction",
    source="Wikipedia contributors, 'Stabilizer code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stabilizer_code",
    prerequisites=["stabilizer_check"],
))
