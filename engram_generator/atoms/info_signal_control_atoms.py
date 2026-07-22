"""Knowledge atoms for information theory, signal processing, and control theory."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Information Theory (tier 5-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="channel_capacity",
    content=(
        "The Shannon-Hartley theorem gives the channel capacity of a "
        "continuous-time analog communication channel subject to Gaussian "
        "noise: C = B * log2(1 + S/N), where C is the channel capacity "
        "in bits per second, B is the bandwidth in hertz, S is the average "
        "signal power, and N is the average noise power. The ratio S/N is "
        "the signal-to-noise ratio (SNR)."
    ),
    example=(
        "Given B=3000 Hz, S/N=1000: "
        "C = 3000 * log2(1 + 1000) = 3000 * log2(1001) = 3000 * 9.967 "
        "= 29901 bits/s"
    ),
    tier=6,
    domain="information_theory",
    source="Wikipedia contributors, 'Shannon-Hartley theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="huffman_coding",
    content=(
        "Huffman coding is an optimal prefix-free coding algorithm. Given "
        "a set of symbols with known frequencies, it builds a binary tree "
        "by repeatedly merging the two least-frequent nodes. The expected "
        "code length L = sum(p_i * l_i) where p_i is the probability and "
        "l_i is the code length for symbol i. Huffman coding achieves the "
        "minimum expected length among all prefix-free codes."
    ),
    example=(
        "Symbols {A:0.4, B:0.3, C:0.2, D:0.1}: "
        "Merge D+C=0.3, then (DC)+B=0.6, then (DCB)+A=1.0. "
        "Codes: A=0, B=10, C=110, D=111. "
        "L = 0.4*1 + 0.3*2 + 0.2*3 + 0.1*3 = 1.9 bits/symbol"
    ),
    tier=5,
    domain="information_theory",
    source="Wikipedia contributors, 'Huffman coding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Huffman_coding",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="hamming_encode",
    content=(
        "Hamming codes are a family of linear error-correcting codes that "
        "can detect up to two-bit errors and correct single-bit errors. "
        "A Hamming(7,4) code encodes 4 data bits into 7 bits by adding "
        "3 parity bits at positions 1, 2, and 4. Each parity bit covers "
        "specific data positions determined by the binary representation "
        "of the position index."
    ),
    example=(
        "Data bits d=[1,0,1,1]: "
        "p1 = d1 xor d2 xor d4 = 1 xor 0 xor 1 = 0, "
        "p2 = d1 xor d3 xor d4 = 1 xor 1 xor 1 = 1, "
        "p4 = d2 xor d3 xor d4 = 0 xor 1 xor 1 = 0. "
        "Encoded: [0,1,1,0,0,1,1]"
    ),
    tier=5,
    domain="information_theory",
    source="Wikipedia contributors, 'Hamming code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hamming_code",
    prerequisites=["binary_arithmetic"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="hamming_decode",
    content=(
        "Hamming decoding computes a syndrome by checking each parity bit. "
        "The syndrome is the binary number formed by the parity check "
        "results. If the syndrome is zero, no error occurred. If non-zero, "
        "the syndrome gives the position of the erroneous bit, which is "
        "then flipped to correct the error."
    ),
    example=(
        "Received [0,1,1,0,1,1,1] (bit 5 flipped from 0 to 1): "
        "s1 = r1 xor r3 xor r5 xor r7 = 0 xor 1 xor 1 xor 1 = 1, "
        "s2 = r2 xor r3 xor r6 xor r7 = 1 xor 1 xor 1 xor 1 = 0, "
        "s4 = r4 xor r5 xor r6 xor r7 = 0 xor 1 xor 1 xor 1 = 1. "
        "Syndrome = 101 = 5, flip bit 5. Corrected: [0,1,1,0,0,1,1]"
    ),
    tier=5,
    domain="information_theory",
    source="Wikipedia contributors, 'Hamming code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hamming_code",
    prerequisites=["hamming_encode"],
))

register_atom(Atom(
    atom_type="theorem",
    name="source_coding",
    content=(
        "Shannon's source coding theorem (noiseless coding theorem) "
        "states that the minimum average number of bits per symbol needed "
        "to encode a source is given by its entropy: H(X) = -sum(p_i * "
        "log2(p_i)). No lossless compression scheme can compress the "
        "source below its entropy rate, and there exist schemes that "
        "approach this limit arbitrarily closely."
    ),
    example=(
        "Source with P(A)=0.5, P(B)=0.25, P(C)=0.125, P(D)=0.125: "
        "H = -(0.5*log2(0.5) + 0.25*log2(0.25) + 0.125*log2(0.125) "
        "+ 0.125*log2(0.125)) = -(0.5*(-1) + 0.25*(-2) + 0.125*(-3) "
        "+ 0.125*(-3)) = 1.75 bits/symbol"
    ),
    tier=5,
    domain="information_theory",
    source="Wikipedia contributors, 'Shannon's source coding theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shannon%27s_source_coding_theorem",
    prerequisites=["info_entropy"],
))

register_atom(Atom(
    atom_type="formula",
    name="error_rate",
    content=(
        "The bit error rate (BER) is the number of bit errors divided by "
        "the total number of bits transferred during a studied time "
        "interval. For binary symmetric channels with crossover "
        "probability p, the probability of an uncorrectable error in a "
        "block of n bits with t-error-correcting code is "
        "P_e = sum(C(n,k)*p^k*(1-p)^(n-k), k=t+1..n)."
    ),
    example=(
        "BSC with p=0.01, n=7, t=1 (Hamming code): "
        "P(0 errors) = (0.99)^7 = 0.9321, "
        "P(1 error) = 7*0.01*(0.99)^6 = 0.0659, "
        "P(uncorrectable) = 1 - 0.9321 - 0.0659 = 0.0020"
    ),
    tier=5,
    domain="information_theory",
    source="Wikipedia contributors, 'Bit error rate', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bit_error_rate",
    prerequisites=["binomial_dist"],
))


# =========================================================================
# Signal Processing (tier 5-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="dft_compute",
    content=(
        "The Discrete Fourier Transform (DFT) converts a finite sequence "
        "of equally-spaced samples into a same-length sequence of "
        "equally-spaced frequency components: X[k] = sum(x[n] * "
        "exp(-j*2*pi*k*n/N), n=0..N-1) for k=0..N-1, where N is the "
        "number of samples, x[n] is the input signal, and X[k] is the "
        "k-th frequency bin."
    ),
    example=(
        "x = [1, 0, -1, 0] (N=4): "
        "X[0] = 1+0+(-1)+0 = 0, "
        "X[1] = 1+0*(-j)+(-1)*(-1)+0*(j) = 1+1 = 2, "
        "X[2] = 1+0+(-1)+0 = 0, "
        "X[3] = 1+0*(j)+(-1)*(-1)+0*(-j) = 2. "
        "DFT = [0, 2, 0, 2]"
    ),
    tier=6,
    domain="signal_processing",
    source="Wikipedia contributors, 'Discrete Fourier transform', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Discrete_Fourier_transform",
    prerequisites=["complex_division"],
))

register_atom(Atom(
    atom_type="theorem",
    name="sampling_theorem",
    content=(
        "The Nyquist-Shannon sampling theorem states that a bandlimited "
        "continuous-time signal can be perfectly reconstructed from its "
        "samples if the sampling rate f_s is at least twice the maximum "
        "frequency component f_max: f_s >= 2*f_max. The minimum sampling "
        "rate 2*f_max is called the Nyquist rate. Sampling below this "
        "rate causes aliasing."
    ),
    example=(
        "Signal with max frequency 4 kHz: "
        "Nyquist rate = 2 * 4000 = 8000 Hz. "
        "CD audio uses 44100 Hz for signals up to 22050 Hz. "
        "If sampled at 6000 Hz (below Nyquist), a 4 kHz tone aliases to "
        "6000 - 4000 = 2 kHz"
    ),
    tier=5,
    domain="signal_processing",
    source="Wikipedia contributors, 'Nyquist-Shannon sampling theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="fir_filter",
    content=(
        "A finite impulse response (FIR) filter computes the output y[n] "
        "as a weighted sum of current and past input values: "
        "y[n] = sum(b_k * x[n-k], k=0..M) where b_k are the filter "
        "coefficients and M is the filter order. FIR filters are always "
        "stable and can be designed to have linear phase."
    ),
    example=(
        "3-tap FIR with b=[0.25, 0.5, 0.25], input x=[1,2,3,4,5]: "
        "y[0] = 0.25*1 = 0.25, "
        "y[1] = 0.25*2 + 0.5*1 = 1.0, "
        "y[2] = 0.25*3 + 0.5*2 + 0.25*1 = 2.0, "
        "y[3] = 0.25*4 + 0.5*3 + 0.25*2 = 3.0"
    ),
    tier=5,
    domain="signal_processing",
    source="Wikipedia contributors, 'Finite impulse response', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Finite_impulse_response",
    prerequisites=["convolution"],
))

register_atom(Atom(
    atom_type="formula",
    name="z_transform",
    content=(
        "The Z-transform converts a discrete-time signal x[n] into a "
        "complex frequency-domain representation: X(z) = sum(x[n] * "
        "z^(-n), n=-inf..inf). For causal signals, the sum starts at "
        "n=0. The Z-transform is the discrete-time equivalent of the "
        "Laplace transform. Poles of X(z) inside the unit circle indicate "
        "a stable system."
    ),
    example=(
        "x[n] = a^n * u[n] (causal exponential): "
        "X(z) = sum(a^n * z^(-n), n=0..inf) = sum((a/z)^n) "
        "= 1/(1 - a*z^(-1)) = z/(z-a) for |z| > |a|. "
        "For a=0.5: X(z) = z/(z-0.5), pole at z=0.5 (stable)"
    ),
    tier=6,
    domain="signal_processing",
    source="Wikipedia contributors, 'Z-transform', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Z-transform",
    prerequisites=["geometric_sequence"],
))

register_atom(Atom(
    atom_type="formula",
    name="transfer_function_signal",
    content=(
        "The transfer function H(z) of a discrete-time LTI system relates "
        "the Z-transforms of input and output: H(z) = Y(z)/X(z). For a "
        "system with FIR coefficients b and IIR coefficients a: "
        "H(z) = (b0 + b1*z^(-1) + ... + bM*z^(-M)) / "
        "(1 + a1*z^(-1) + ... + aN*z^(-N)). The frequency response is "
        "obtained by evaluating H(e^(j*omega))."
    ),
    example=(
        "First-order IIR: y[n] = x[n] + 0.5*y[n-1]. "
        "H(z) = 1/(1 - 0.5*z^(-1)) = z/(z - 0.5). "
        "Pole at z=0.5 (inside unit circle, stable). "
        "|H(e^(j*0))| = 1/(1-0.5) = 2 (DC gain)"
    ),
    tier=6,
    domain="signal_processing",
    source="Wikipedia contributors, 'Transfer function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transfer_function",
    prerequisites=["z_transform"],
))

register_atom(Atom(
    atom_type="formula",
    name="frequency_response",
    content=(
        "The frequency response H(e^(j*omega)) of a discrete-time system "
        "is obtained by evaluating its transfer function on the unit "
        "circle. The magnitude response |H(e^(j*omega))| gives the gain "
        "at frequency omega, and the phase response arg(H(e^(j*omega))) "
        "gives the phase shift. For an FIR filter with coefficients b_k: "
        "H(e^(j*omega)) = sum(b_k * e^(-j*k*omega))."
    ),
    example=(
        "2-tap averaging filter b=[0.5, 0.5]: "
        "H(e^(j*omega)) = 0.5 + 0.5*e^(-j*omega) "
        "= 0.5*e^(-j*omega/2)*(e^(j*omega/2) + e^(-j*omega/2)) "
        "= e^(-j*omega/2)*cos(omega/2). "
        "|H| at omega=0: cos(0)=1, at omega=pi: cos(pi/2)=0"
    ),
    tier=6,
    domain="signal_processing",
    source="Wikipedia contributors, 'Frequency response', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Frequency_response",
    prerequisites=["transfer_function_signal"],
))


# =========================================================================
# Control Theory (tier 5-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="transfer_function_sys",
    content=(
        "In control theory, the transfer function G(s) of a continuous-time "
        "LTI system is the ratio of the Laplace transform of the output "
        "to the Laplace transform of the input, assuming zero initial "
        "conditions: G(s) = Y(s)/U(s). For a standard second-order system: "
        "G(s) = omega_n^2 / (s^2 + 2*zeta*omega_n*s + omega_n^2), where "
        "omega_n is the natural frequency and zeta is the damping ratio."
    ),
    example=(
        "Mass-spring-damper: m=1kg, c=4Ns/m, k=3N/m. "
        "G(s) = 1/(s^2 + 4s + 3) = 1/((s+1)(s+3)). "
        "Poles at s=-1, s=-3 (both negative, stable). "
        "DC gain: G(0) = 1/3"
    ),
    tier=5,
    domain="control_theory",
    source="Wikipedia contributors, 'Transfer function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transfer_function",
    prerequisites=["laplace_transform"],
))

register_atom(Atom(
    atom_type="formula",
    name="pid_response",
    content=(
        "A PID controller computes a control signal u(t) from the error "
        "e(t) = setpoint - measured: u(t) = K_p*e(t) + K_i*integral(e) "
        "+ K_d*de/dt. In the Laplace domain: C(s) = K_p + K_i/s + K_d*s. "
        "K_p is the proportional gain (reduces steady-state error), "
        "K_i is the integral gain (eliminates steady-state error), and "
        "K_d is the derivative gain (reduces overshoot)."
    ),
    example=(
        "PID with K_p=2, K_i=1, K_d=0.5: "
        "C(s) = 2 + 1/s + 0.5*s = (0.5*s^2 + 2*s + 1)/s. "
        "At t=0, e=10, de/dt=0, integral(e)=0: "
        "u = 2*10 + 1*0 + 0.5*0 = 20"
    ),
    tier=5,
    domain="control_theory",
    source="Wikipedia contributors, 'PID controller', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/PID_controller",
    prerequisites=["transfer_function_sys"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="stability_routh",
    content=(
        "The Routh-Hurwitz stability criterion determines system stability "
        "from the characteristic polynomial coefficients without computing "
        "roots. For polynomial a_n*s^n + a_(n-1)*s^(n-1) + ... + a_0, "
        "construct the Routh array. The system is stable if and only if "
        "all elements in the first column of the Routh array are positive "
        "(for a polynomial with positive leading coefficient)."
    ),
    example=(
        "Characteristic polynomial: s^3 + 2s^2 + 3s + 6. "
        "Row s^3: [1, 3], Row s^2: [2, 6]. "
        "Row s^1: [(2*3 - 1*6)/2, 0] = [0, 0]. "
        "Zero row indicates marginal stability (imaginary roots). "
        "Auxiliary: 2s^2 + 6 = 0, s = +/-j*sqrt(3)"
    ),
    tier=6,
    domain="control_theory",
    source="Wikipedia contributors, 'Routh-Hurwitz stability criterion', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Routh%E2%80%93Hurwitz_stability_criterion",
    prerequisites=["transfer_function_sys"],
))

register_atom(Atom(
    atom_type="formula",
    name="bode_magnitude",
    content=(
        "A Bode plot represents the frequency response of a system as two "
        "graphs: magnitude (in dB) and phase (in degrees) versus frequency "
        "(log scale). For a transfer function G(jw), the magnitude in "
        "decibels is 20*log10(|G(jw)|). Key features: gain crossover "
        "frequency (where |G|=1 or 0 dB), phase margin (180 + phase at "
        "gain crossover), and gain margin (negative of gain in dB at "
        "phase crossover)."
    ),
    example=(
        "G(s) = 10/(s+1): |G(jw)| = 10/sqrt(1+w^2). "
        "At w=0: 20*log10(10) = 20 dB. "
        "At w=1: 20*log10(10/sqrt(2)) = 20*log10(7.07) = 17 dB. "
        "At w=10: 20*log10(10/sqrt(101)) = 20*log10(0.995) = -0.04 dB"
    ),
    tier=5,
    domain="control_theory",
    source="Wikipedia contributors, 'Bode plot', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bode_plot",
    prerequisites=["transfer_function_sys", "logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="state_space",
    content=(
        "State-space representation describes a system using first-order "
        "differential equations: dx/dt = A*x + B*u, y = C*x + D*u, where "
        "x is the state vector, u is the input vector, y is the output "
        "vector, A is the state matrix, B is the input matrix, C is the "
        "output matrix, and D is the feedthrough matrix. The transfer "
        "function is G(s) = C*(sI - A)^(-1)*B + D."
    ),
    example=(
        "Mass-spring: A=[[0,1],[-3,-4]], B=[[0],[1]], C=[1,0], D=[0]. "
        "Eigenvalues of A: det(A-lambda*I) = lambda^2+4*lambda+3 = 0, "
        "lambda = -1, -3. Both negative: stable. "
        "G(s) = C*(sI-A)^(-1)*B = 1/(s^2+4s+3)"
    ),
    tier=6,
    domain="control_theory",
    source="Wikipedia contributors, 'State-space representation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/State-space_representation",
    prerequisites=["eigenvalue", "matrix_inverse"],
))

register_atom(Atom(
    atom_type="formula",
    name="feedback_gain",
    content=(
        "In a negative feedback control system with forward gain G(s) and "
        "feedback gain H(s), the closed-loop transfer function is "
        "T(s) = G(s) / (1 + G(s)*H(s)). For unity feedback (H=1): "
        "T(s) = G(s) / (1 + G(s)). The loop gain L(s) = G(s)*H(s) "
        "determines stability and performance."
    ),
    example=(
        "G(s) = 10/(s+1), H(s) = 1 (unity feedback): "
        "T(s) = (10/(s+1)) / (1 + 10/(s+1)) = 10/(s+1+10) = 10/(s+11). "
        "DC gain: T(0) = 10/11 = 0.909. "
        "Pole at s=-11 (faster than open-loop pole at s=-1)"
    ),
    tier=5,
    domain="control_theory",
    source="Wikipedia contributors, 'Negative feedback', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Negative_feedback",
    prerequisites=["transfer_function_sys"],
))
