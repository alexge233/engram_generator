"""Knowledge atoms for signal processing ext, solid state ext, and quantum info ext."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Signal Processing Ext (tier 4-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="convolution_continuous",
    content=(
        "The convolution of two continuous functions f and g is defined as "
        "(f * g)(t) = integral from -inf to inf of f(tau) g(t - tau) dtau. "
        "Convolution describes the output of a linear time-invariant system "
        "when the input is convolved with the impulse response."
    ),
    example=(
        "f(t) = e^{-t}u(t), g(t) = u(t) (unit step): "
        "(f*g)(t) = integral_0^t e^{-tau} dtau = 1 - e^{-t} for t >= 0"
    ),
    tier=5,
    domain="signal_processing",
    source="Wikipedia contributors, 'Convolution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convolution",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="correlation_signal",
    content=(
        "Cross-correlation measures the similarity of two signals as a "
        "function of time lag. R_xy(tau) = integral f(t) g(t + tau) dt. "
        "Autocorrelation is the cross-correlation of a signal with itself."
    ),
    example=(
        "Autocorrelation of x(t) = cos(2*pi*t) at lag 0: "
        "R_xx(0) = integral_0^1 cos^2(2*pi*t) dt = 0.5"
    ),
    tier=5,
    domain="signal_processing",
    source="Wikipedia contributors, 'Cross-correlation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cross-correlation",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="nyquist_diagram",
    content=(
        "The Nyquist plot maps the open-loop transfer function G(j*omega) "
        "in the complex plane as omega varies from -inf to inf. The Nyquist "
        "stability criterion counts encirclements of the point -1+0j to "
        "determine closed-loop stability."
    ),
    example=(
        "G(s) = 1/(s+1): G(j*omega) = 1/(j*omega+1). "
        "At omega=0: G=1, at omega=1: G=1/(1+j)=(1-j)/2, |G|=0.707, angle=-45deg. "
        "No encirclements of -1, system is stable."
    ),
    tier=6,
    domain="signal_processing",
    source="Wikipedia contributors, 'Nyquist stability criterion', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nyquist_stability_criterion",
    prerequisites=["transfer_function_sys"],
))

register_atom(Atom(
    atom_type="formula",
    name="bode_plot_compute",
    content=(
        "A Bode plot displays the magnitude (in dB) and phase (in degrees) "
        "of a transfer function H(j*omega) versus frequency. "
        "Magnitude: 20*log10(|H(j*omega)|), Phase: angle(H(j*omega))."
    ),
    example=(
        "H(s) = 10/(s+10): at omega=10, H(j*10) = 10/(10+j*10), "
        "|H| = 10/sqrt(200) = 0.707, 20*log10(0.707) = -3.01 dB, "
        "phase = -arctan(10/10) = -45 deg"
    ),
    tier=5,
    domain="signal_processing",
    source="Wikipedia contributors, 'Bode plot', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bode_plot",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="signal_energy_power",
    content=(
        "Signal energy E = integral_{-inf}^{inf} |x(t)|^2 dt for "
        "energy signals. Signal power P = lim_{T->inf} (1/2T) "
        "integral_{-T}^{T} |x(t)|^2 dt for power signals."
    ),
    example=(
        "x(t) = 3*e^{-2t}*u(t): E = integral_0^inf 9*e^{-4t} dt "
        "= 9/4 = 2.25 joules"
    ),
    tier=4,
    domain="signal_processing",
    source="Wikipedia contributors, 'Energy (signal processing)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Energy_(signal_processing)",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="modulation_demod",
    content=(
        "Amplitude modulation (AM) produces s(t) = [1 + m*cos(2*pi*f_m*t)] "
        "* cos(2*pi*f_c*t), where m is the modulation index, f_m the "
        "message frequency, and f_c the carrier frequency."
    ),
    example=(
        "f_c=1000Hz, f_m=100Hz, m=0.5: at t=0, s(0) = (1+0.5)*1 = 1.5. "
        "Bandwidth = 2*f_m = 200 Hz"
    ),
    tier=5,
    domain="signal_processing",
    source="Wikipedia contributors, 'Amplitude modulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Amplitude_modulation",
    prerequisites=["sin_cos_eval"],
))

register_atom(Atom(
    atom_type="formula",
    name="matched_filter",
    content=(
        "A matched filter maximises the output signal-to-noise ratio (SNR) "
        "for a known signal in additive white Gaussian noise. The impulse "
        "response is h(t) = s(T-t), a time-reversed and delayed copy of "
        "the signal template."
    ),
    example=(
        "Signal s(t) = rect(t) (pulse of width 1): matched filter "
        "h(t) = rect(T-t). Output SNR = 2*E/N_0, where E = 1 (energy of "
        "unit pulse). For N_0 = 0.1: SNR = 20 = 13 dB"
    ),
    tier=6,
    domain="signal_processing",
    source="Wikipedia contributors, 'Matched filter', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Matched_filter",
    prerequisites=["convolution_continuous"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="sigma_delta",
    content=(
        "Sigma-delta (oversampling) modulation converts an analog signal to "
        "a 1-bit digital stream at a high sample rate, then decimates to the "
        "target rate. The quantization noise is shaped to high frequencies by "
        "the feedback loop, achieving high resolution in-band."
    ),
    example=(
        "Input DC = 0.3, 1-bit quantizer: output stream approximates 0.3 "
        "by producing '1' roughly 65% of the time and '0' 35% of the time. "
        "At OSR=64, effective bits ~ 0.5*log2(64^3) ~ 9 bits"
    ),
    tier=5,
    domain="signal_processing",
    source="Wikipedia contributors, 'Delta-sigma modulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Delta-sigma_modulation",
    prerequisites=["sampling_theorem"],
))


# ---------------------------------------------------------------------------
# Solid State Ext (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="effective_mass",
    content=(
        "The effective mass m* of a charge carrier in a crystal is defined "
        "by 1/m* = (1/hbar^2) * d^2E/dk^2, where E(k) is the energy "
        "dispersion relation. It accounts for the periodic potential of the "
        "lattice, allowing carriers to be treated as free particles with "
        "modified mass."
    ),
    example=(
        "For E(k) = hbar^2*k^2/(2*m_0) + E_gap (free electron-like): "
        "d^2E/dk^2 = hbar^2/m_0, so m* = m_0 (free electron mass)"
    ),
    tier=5,
    domain="solid_state_physics",
    source="Wikipedia contributors, 'Effective mass (solid-state physics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Effective_mass_(solid-state_physics)",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="density_of_states",
    content=(
        "The density of states g(E) gives the number of available quantum "
        "states per unit energy per unit volume. For a 3D free electron gas: "
        "g(E) = (1/2*pi^2) * (2*m/hbar^2)^{3/2} * sqrt(E)."
    ),
    example=(
        "For free electrons at E = 1 eV (1.6e-19 J): "
        "g(E) = (1/(2*pi^2)) * (2*9.11e-31/1.055e-34^2)^1.5 * sqrt(1.6e-19) "
        "= 1.06e47 states/(J*m^3)"
    ),
    tier=5,
    domain="solid_state_physics",
    source="Wikipedia contributors, 'Density of states', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Density_of_states",
    prerequisites=["integration_by_substitution"],
))

register_atom(Atom(
    atom_type="formula",
    name="semiconductor_doping",
    content=(
        "In an n-type semiconductor with donor concentration N_D, the "
        "electron concentration n approx N_D at room temperature (full "
        "ionisation). The Fermi level shifts toward the conduction band: "
        "E_F = E_C - k_B*T*ln(N_C/N_D), where N_C is the effective "
        "density of states in the conduction band."
    ),
    example=(
        "Si at 300K: N_C = 2.8e25 m^-3, N_D = 1e22 m^-3. "
        "E_F - E_C = -0.0259 * ln(2.8e25/1e22) = -0.0259 * 7.937 "
        "= -0.2056 eV (Fermi level 0.206 eV below conduction band)"
    ),
    tier=5,
    domain="solid_state_physics",
    source="Wikipedia contributors, 'Doping (semiconductor)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Doping_(semiconductor)",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="dielectric_constant",
    content=(
        "The capacitance of a parallel-plate capacitor filled with a "
        "dielectric material of relative permittivity epsilon_r is "
        "C = epsilon_r * epsilon_0 * A / d, where A is the plate area "
        "and d the plate separation."
    ),
    example=(
        "Glass (epsilon_r=5), A=0.01 m^2, d=0.001 m: "
        "C = 5 * 8.854e-12 * 0.01 / 0.001 = 4.427e-10 F = 0.4427 nF"
    ),
    tier=4,
    domain="solid_state_physics",
    source="Wikipedia contributors, 'Capacitance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Capacitance",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="magnetic_susceptibility",
    content=(
        "Magnetic susceptibility chi relates the magnetisation M to the "
        "applied magnetic field H: M = chi * H. For paramagnetic materials, "
        "Curie's law gives chi = C/T, where C is the Curie constant and T "
        "the temperature."
    ),
    example=(
        "Paramagnetic salt with C = 0.5 K at T = 300 K: "
        "chi = 0.5/300 = 1.667e-3 (dimensionless, SI)"
    ),
    tier=5,
    domain="solid_state_physics",
    source="Wikipedia contributors, 'Magnetic susceptibility', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Magnetic_susceptibility",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="crystal_momentum",
    content=(
        "Crystal momentum is p = hbar * k, where k is the wave vector "
        "in the Brillouin zone. Unlike true momentum, crystal momentum "
        "is conserved modulo a reciprocal lattice vector G: "
        "k_final = k_initial + q + G."
    ),
    example=(
        "Electron with k = pi/a at zone boundary (a = 5e-10 m): "
        "p = 1.055e-34 * pi/(5e-10) = 6.63e-25 kg*m/s"
    ),
    tier=5,
    domain="solid_state_physics",
    source="Wikipedia contributors, 'Crystal momentum', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Crystal_momentum",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="superconductor_tc",
    content=(
        "BCS theory predicts the critical temperature T_c of a "
        "superconductor as k_B * T_c approx 1.13 * hbar * omega_D * "
        "exp(-1/(N(0)*V)), where omega_D is the Debye frequency, N(0) "
        "the density of states at the Fermi level, and V the electron-phonon "
        "coupling constant."
    ),
    example=(
        "For N(0)*V = 0.3, hbar*omega_D/k_B = 300 K: "
        "T_c = 1.13 * 300 * exp(-1/0.3) = 339 * exp(-3.33) "
        "= 339 * 0.0357 = 12.1 K"
    ),
    tier=5,
    domain="solid_state_physics",
    source="Wikipedia contributors, 'BCS theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/BCS_theory",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="lattice_vibration",
    content=(
        "The dispersion relation for a monatomic 1D lattice with spring "
        "constant K, mass m, and lattice constant a is: "
        "omega(k) = 2*sqrt(K/m) * |sin(k*a/2)|. The maximum frequency "
        "(Debye cutoff) is omega_max = 2*sqrt(K/m)."
    ),
    example=(
        "K = 10 N/m, m = 1e-26 kg, a = 3e-10 m: "
        "omega_max = 2*sqrt(10/1e-26) = 2*sqrt(1e27) = 2*3.16e13 "
        "= 6.32e13 rad/s"
    ),
    tier=5,
    domain="solid_state_physics",
    source="Wikipedia contributors, 'Phonon', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Phonon",
    prerequisites=["sin_cos_eval"],
))


# ---------------------------------------------------------------------------
# Quantum Information Ext (tier 6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="quantum_circuit",
    content=(
        "A quantum circuit is a sequence of quantum gates applied to qubits. "
        "Common gates: Hadamard H = (1/sqrt(2))[[1,1],[1,-1]], "
        "Pauli-X (NOT) = [[0,1],[1,0]], CNOT (2-qubit controlled-NOT). "
        "The output state is computed by matrix multiplication of gate "
        "matrices on the input state vector."
    ),
    example=(
        "H|0> = (1/sqrt(2))(|0>+|1>), then CNOT on qubits 1,2: "
        "CNOT(H|0> tensor |0>) = (1/sqrt(2))(|00>+|11>) = Bell state"
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Quantum circuit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantum_circuit",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="formula",
    name="quantum_measurement",
    content=(
        "A projective measurement in basis {|m>} on state |psi> yields "
        "outcome m with probability p(m) = |<m|psi>|^2 (Born rule). "
        "After measurement, the state collapses to |m>."
    ),
    example=(
        "|psi> = (3/5)|0> + (4/5)|1>: "
        "p(0) = |3/5|^2 = 9/25 = 0.36, "
        "p(1) = |4/5|^2 = 16/25 = 0.64"
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Measurement in quantum mechanics', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Measurement_in_quantum_mechanics",
    prerequisites=["basic_prob"],
))

register_atom(Atom(
    atom_type="formula",
    name="quantum_entropy",
    content=(
        "The von Neumann entropy of a quantum state rho is "
        "S(rho) = -Tr(rho * log2(rho)). For a pure state, S = 0. "
        "For a maximally mixed state of dimension d, S = log2(d)."
    ),
    example=(
        "Maximally mixed 2-qubit state: rho = I/4, "
        "S = -Tr((I/4)*log2(I/4)) = -4*(1/4)*log2(1/4) = 2 bits"
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Von Neumann entropy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Von_Neumann_entropy",
    prerequisites=["info_entropy"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="superdense_coding",
    content=(
        "Superdense coding allows transmitting 2 classical bits by sending "
        "1 qubit, using a shared Bell pair. Alice applies one of {I, X, Z, "
        "XZ} to her qubit encoding 2 bits, then sends it to Bob who performs "
        "a Bell measurement to decode."
    ),
    example=(
        "To send '10': Alice applies Z to her half of |Phi+>, producing "
        "|Phi-> = (1/sqrt(2))(|00>-|11>). Bob measures in Bell basis, "
        "gets |Phi-> -> decodes '10'"
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Superdense coding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Superdense_coding",
    prerequisites=["quantum_gate"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="quantum_key_dist",
    content=(
        "BB84 quantum key distribution protocol: Alice sends qubits in "
        "random bases (Z or X). Bob measures in random bases. They publicly "
        "compare bases and keep only matching-basis bits. An eavesdropper "
        "introduces detectable errors (QBER > 11% indicates Eve)."
    ),
    example=(
        "Alice sends |0> in Z-basis, Bob measures in Z-basis: gets 0 (keep). "
        "Alice sends |+> in X-basis, Bob measures in Z-basis: random result "
        "(discard). After 100 rounds with 50 matching bases, ~25 key bits."
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'BB84', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/BB84",
    prerequisites=["quantum_measurement"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="swap_test",
    content=(
        "The SWAP test determines the overlap |<psi|phi>|^2 between two "
        "quantum states without full tomography. Using an ancilla qubit, "
        "Hadamard, controlled-SWAP, and Hadamard again, the probability of "
        "measuring |0> on the ancilla is P(0) = (1 + |<psi|phi>|^2)/2."
    ),
    example=(
        "If |psi> = |0>, |phi> = |0> (identical): "
        "|<psi|phi>|^2 = 1, P(0) = (1+1)/2 = 1. "
        "If |psi> = |0>, |phi> = |1> (orthogonal): "
        "|<psi|phi>|^2 = 0, P(0) = 1/2."
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Swap test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Swap_test",
    prerequisites=["quantum_circuit"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="quantum_walk",
    content=(
        "A discrete-time quantum walk on a line uses a coin operator "
        "(e.g. Hadamard) and a conditional shift operator. Unlike classical "
        "random walks that spread as sqrt(t), quantum walks spread linearly "
        "in t, giving a quadratic speedup for search problems."
    ),
    example=(
        "Hadamard coin on a line, starting at origin |0>|R>: "
        "after t=10 steps, the probability distribution has peaks near "
        "positions +/-7 (not Gaussian), variance ~ t^2/2 = 50"
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Quantum walk', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantum_walk",
    prerequisites=["random_walk"],
))

register_atom(Atom(
    atom_type="formula",
    name="fidelity",
    content=(
        "The fidelity between two quantum states rho and sigma measures "
        "their closeness: F(rho, sigma) = (Tr(sqrt(sqrt(rho)*sigma*sqrt(rho))))^2. "
        "For pure states: F(|psi>, |phi>) = |<psi|phi>|^2. "
        "F = 1 for identical states, F = 0 for orthogonal states."
    ),
    example=(
        "|psi> = |0>, |phi> = cos(pi/6)|0> + sin(pi/6)|1>: "
        "F = |<0|(cos(30)|0>+sin(30)|1>)|^2 = cos^2(30) = 3/4 = 0.75"
    ),
    tier=6,
    domain="quantum_information",
    source="Wikipedia contributors, 'Fidelity of quantum states', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fidelity_of_quantum_states",
    prerequisites=["quantum_measurement"],
))
