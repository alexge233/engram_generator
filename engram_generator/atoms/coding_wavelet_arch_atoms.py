"""Knowledge atoms for coding theory, wavelet theory, and computer architecture."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Coding theory (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="concept",
    name="linear_code",
    content=(
        "A linear code C(n, k) over GF(q) is a k-dimensional subspace "
        "of GF(q)^n. It is defined by a generator matrix G (k x n) or "
        "a parity-check matrix H ((n-k) x n) such that H * c^T = 0 for "
        "every codeword c. The minimum distance d determines error "
        "correction capability: corrects floor((d-1)/2) errors."
    ),
    example=(
        "Hamming(7,4): G = [I_4 | P] where P is the 4x3 parity matrix. "
        "Message [1,0,1,1] -> codeword [1,0,1,1,0,1,0]. d=3, corrects 1 error."
    ),
    tier=5,
    domain="coding_theory",
    source="Wikipedia contributors, 'Linear code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Linear_code",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="syndrome_decode",
    content=(
        "Syndrome decoding computes s = H * r^T for received word r. "
        "If s = 0, no error detected. Otherwise, s matches a column of H, "
        "identifying the error position. For a Hamming code, the syndrome "
        "is the binary representation of the error position."
    ),
    example=(
        "Hamming(7,4): received r = [1,0,1,1,0,0,0]. "
        "s = H*r^T = [1,1,0]^T = column 6 of H. "
        "Error at position 6: corrected = [1,0,1,1,0,1,0]."
    ),
    tier=5,
    domain="coding_theory",
    source="Wikipedia contributors, 'Syndrome decoding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Decoding_methods#Syndrome_decoding",
    prerequisites=["linear_code"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="bch_encode",
    content=(
        "BCH codes are cyclic error-correcting codes defined by a "
        "generator polynomial g(x) that is the LCM of minimal polynomials "
        "of consecutive powers of a primitive element. Encoding: multiply "
        "message polynomial m(x) by x^(n-k), divide by g(x), append remainder."
    ),
    example=(
        "BCH(15,7,2): g(x) has degree 8. Message m(x) = x^6 + x^4 + 1. "
        "m(x)*x^8 mod g(x) gives remainder r(x). Codeword = m(x)*x^8 + r(x)."
    ),
    tier=6,
    domain="coding_theory",
    source="Wikipedia contributors, 'BCH code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/BCH_code",
    prerequisites=["polynomial_multiply"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="reed_solomon",
    content=(
        "Reed-Solomon codes RS(n, k) over GF(2^m) are a subclass of "
        "BCH codes that can correct up to t = (n-k)/2 symbol errors. "
        "Encoding evaluates a message polynomial at n points. Decoding "
        "uses the Berlekamp-Massey algorithm to find the error-locator "
        "polynomial."
    ),
    example=(
        "RS(255, 223) over GF(2^8): corrects up to 16 symbol errors. "
        "Used in CDs, DVDs, QR codes, and deep-space communication."
    ),
    tier=6,
    domain="coding_theory",
    source="Wikipedia contributors, 'Reed-Solomon error correction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction",
    prerequisites=["bch_encode"],
))

register_atom(Atom(
    atom_type="formula",
    name="code_parameters",
    content=(
        "The parameters of an [n, k, d] code are: n = block length, "
        "k = message length, d = minimum Hamming distance. The code "
        "rate R = k/n. The Singleton bound gives d <= n - k + 1. "
        "Codes meeting this bound are called maximum distance separable (MDS)."
    ),
    example=(
        "Hamming(7,4): n=7, k=4, d=3. R = 4/7 = 0.571. "
        "Singleton bound: d <= 7-4+1 = 4. Actual d=3 < 4, not MDS."
    ),
    tier=5,
    domain="coding_theory",
    source="Wikipedia contributors, 'Singleton bound', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Singleton_bound",
    prerequisites=["linear_code"],
))

register_atom(Atom(
    atom_type="concept",
    name="turbo_code_interleave",
    content=(
        "Turbo codes use two parallel convolutional encoders separated "
        "by an interleaver that permutes the input bits. The interleaver "
        "creates statistical independence between the two parity sequences, "
        "enabling iterative decoding to approach the Shannon limit."
    ),
    example=(
        "Rate-1/3 turbo code: 4-bit message [1,0,1,1]. "
        "Encoder 1 output: [1,1,0,1]. Interleaved: [1,1,0,1]. "
        "Encoder 2 output: [0,1,1,0]. Transmitted: message + both parities."
    ),
    tier=6,
    domain="coding_theory",
    source="Wikipedia contributors, 'Turbo code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Turbo_code",
    prerequisites=["linear_code"],
))

# ---------------------------------------------------------------------------
# Wavelet theory (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="haar_wavelet_decompose",
    content=(
        "The Haar wavelet decomposition splits a signal into approximation "
        "and detail coefficients: a_k = (x_{2k} + x_{2k+1}) / sqrt(2), "
        "d_k = (x_{2k} - x_{2k+1}) / sqrt(2). Recursively applied to "
        "approximation coefficients for multi-level decomposition."
    ),
    example=(
        "Signal [4, 6, 10, 12]: "
        "a = [(4+6)/sqrt(2), (10+12)/sqrt(2)] = [7.071, 15.556]. "
        "d = [(4-6)/sqrt(2), (10-12)/sqrt(2)] = [-1.414, -1.414]."
    ),
    tier=5,
    domain="wavelet_theory",
    source="Wikipedia contributors, 'Haar wavelet', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Haar_wavelet",
    prerequisites=["summation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="haar_reconstruct",
    content=(
        "Haar wavelet reconstruction reverses the decomposition: "
        "x_{2k} = (a_k + d_k) / sqrt(2), x_{2k+1} = (a_k - d_k) / sqrt(2). "
        "Perfect reconstruction is guaranteed when the analysis and "
        "synthesis filters satisfy the biorthogonality condition."
    ),
    example=(
        "a = [7.071, 15.556], d = [-1.414, -1.414]: "
        "x_0 = (7.071-1.414)/sqrt(2) = 4, x_1 = (7.071+1.414)/sqrt(2) = 6, "
        "x_2 = (15.556-1.414)/sqrt(2) = 10, x_3 = (15.556+1.414)/sqrt(2) = 12."
    ),
    tier=5,
    domain="wavelet_theory",
    source="Wikipedia contributors, 'Haar wavelet', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Haar_wavelet",
    prerequisites=["haar_wavelet_decompose"],
))

register_atom(Atom(
    atom_type="concept",
    name="multiresolution",
    content=(
        "Multiresolution analysis (MRA) provides a framework for wavelets "
        "as a nested sequence of subspaces V_j that satisfy: "
        "V_j subset V_{j+1}, union V_j = L^2(R), intersection V_j = {0}. "
        "A scaling function phi generates V_0, and the wavelet psi "
        "generates the orthogonal complement W_0 = V_1 - V_0."
    ),
    example=(
        "Haar MRA: V_0 = piecewise constant on [n, n+1). "
        "V_1 = piecewise constant on [n/2, (n+1)/2). "
        "W_0 captures detail lost going from V_1 to V_0."
    ),
    tier=6,
    domain="wavelet_theory",
    source="Wikipedia contributors, 'Multiresolution analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Multiresolution_analysis",
    prerequisites=["haar_wavelet_decompose"],
))

register_atom(Atom(
    atom_type="formula",
    name="wavelet_energy",
    content=(
        "The energy of a signal at wavelet scale j is the sum of squared "
        "detail coefficients: E_j = sum_k |d_{j,k}|^2. By Parseval's "
        "theorem, the total energy equals the sum of energies across all "
        "scales: E = sum_j E_j + E_approx."
    ),
    example=(
        "Detail coefficients d = [-1.414, -1.414]: "
        "E = 1.414^2 + 1.414^2 = 2 + 2 = 4."
    ),
    tier=5,
    domain="wavelet_theory",
    source="Wikipedia contributors, 'Wavelet', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Wavelet",
    prerequisites=["summation"],
))

register_atom(Atom(
    atom_type="concept",
    name="filter_bank",
    content=(
        "A filter bank decomposes a signal using lowpass (scaling) and "
        "highpass (wavelet) filters followed by downsampling by 2. "
        "The lowpass filter h[n] and highpass filter g[n] are related by "
        "g[n] = (-1)^n * h[1-n] (quadrature mirror filter). Perfect "
        "reconstruction requires |H(z)|^2 + |H(-z)|^2 = 2."
    ),
    example=(
        "Haar filters: h = [1/sqrt(2), 1/sqrt(2)], "
        "g = [1/sqrt(2), -1/sqrt(2)]. "
        "Signal [3, 7]: lowpass = (3+7)/sqrt(2) = 7.07, "
        "highpass = (3-7)/sqrt(2) = -2.83."
    ),
    tier=6,
    domain="wavelet_theory",
    source="Wikipedia contributors, 'Filter bank', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Filter_bank",
    prerequisites=["convolution"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="thresholding",
    content=(
        "Wavelet thresholding (denoising) sets small detail coefficients "
        "to zero. Hard thresholding: d' = d if |d| > t, else 0. "
        "Soft thresholding: d' = sign(d)(|d| - t) if |d| > t, else 0. "
        "The universal threshold t = sigma * sqrt(2 * ln(n)) is "
        "asymptotically optimal (Donoho and Johnstone, 1994)."
    ),
    example=(
        "Coefficients [3.2, -0.5, 1.8, -0.2], threshold t = 1.0. "
        "Hard: [3.2, 0, 1.8, 0]. Soft: [2.2, 0, 0.8, 0]."
    ),
    tier=5,
    domain="wavelet_theory",
    source="Wikipedia contributors, 'Wavelet denoising', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Wavelet_denoising",
    prerequisites=["haar_wavelet_decompose"],
))

# ---------------------------------------------------------------------------
# Computer architecture (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="pipeline_throughput",
    content=(
        "In a k-stage pipeline processing n instructions, the total time "
        "is T = (k + n - 1) * t_stage, where t_stage is the clock period. "
        "Throughput = n / T. Speedup over non-pipelined execution: "
        "S = k * n / (k + n - 1), approaching k for large n."
    ),
    example=(
        "5-stage pipeline, 100 instructions, t_stage = 1 ns: "
        "T = (5+100-1)*1 = 104 ns. Throughput = 100/104 = 0.962 instr/ns. "
        "Speedup = 5*100/104 = 4.81x."
    ),
    tier=4,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Instruction pipelining', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Instruction_pipelining",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="cache_hit_ratio",
    content=(
        "The cache hit ratio h = hits / (hits + misses). The effective "
        "memory access time is T_eff = h * T_cache + (1-h) * T_mem. "
        "A higher hit ratio dramatically reduces average access time "
        "since T_cache << T_mem (typically 1ns vs 100ns)."
    ),
    example=(
        "95 hits, 5 misses: h = 95/100 = 0.95. "
        "T_cache = 1ns, T_mem = 100ns. "
        "T_eff = 0.95*1 + 0.05*100 = 0.95 + 5 = 5.95 ns."
    ),
    tier=4,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Cache (computing)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cache_(computing)#Cache_performance",
    prerequisites=["percentage"],
))

register_atom(Atom(
    atom_type="concept",
    name="branch_prediction",
    content=(
        "Branch prediction guesses the outcome of conditional branches "
        "before they are resolved, keeping the pipeline full. A 2-bit "
        "saturating counter uses states {strongly not taken, weakly not "
        "taken, weakly taken, strongly taken}. Prediction accuracy "
        "typically 90-97% on modern processors."
    ),
    example=(
        "2-bit counter starts at 'weakly taken' (10). Branch taken -> "
        "'strongly taken' (11). Branch not taken -> 'weakly taken' (10). "
        "Prediction: taken when state >= 10."
    ),
    tier=5,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Branch predictor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Branch_predictor",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="concept",
    name="instruction_scheduling",
    content=(
        "Instruction scheduling reorders instructions to minimise "
        "pipeline stalls from data hazards while preserving program "
        "semantics. List scheduling assigns priorities (e.g., critical "
        "path length) and greedily schedules instructions when their "
        "operands are available."
    ),
    example=(
        "Instructions: A: r1 = r2 + r3, B: r4 = r1 * 2, C: r5 = r6 + r7. "
        "B depends on A (data hazard). C is independent. "
        "Schedule: A, C, B (C fills the stall slot)."
    ),
    tier=5,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Instruction scheduling', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Instruction_scheduling",
    prerequisites=["topo_sort"],
))

register_atom(Atom(
    atom_type="concept",
    name="memory_hierarchy",
    content=(
        "The memory hierarchy trades off speed, size, and cost across "
        "levels: registers (< 1ns, bytes), L1 cache (1-2ns, KB), "
        "L2/L3 cache (5-20ns, MB), main memory (50-100ns, GB), "
        "SSD (50-100us, TB), HDD (5-10ms, TB). Locality of reference "
        "(temporal and spatial) makes caching effective."
    ),
    example=(
        "L1 = 32KB (1ns), L2 = 256KB (5ns), RAM = 16GB (100ns). "
        "With 90% L1 hit, 95% L2 hit of L1 misses: "
        "T_avg = 0.9*1 + 0.1*0.95*5 + 0.1*0.05*100 = 0.9+0.475+0.5 = 1.875 ns."
    ),
    tier=4,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Memory hierarchy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Memory_hierarchy",
    prerequisites=["cache_hit_ratio"],
))

register_atom(Atom(
    atom_type="law",
    name="amdahl_speedup",
    content=(
        "Amdahl's law gives the theoretical speedup of a program using "
        "p processors: S(p) = 1 / ((1 - f) + f/p), where f is the "
        "fraction of the program that can be parallelised. As p -> infinity, "
        "S_max = 1 / (1 - f). A program that is 95% parallelisable can "
        "achieve at most 20x speedup."
    ),
    example=(
        "f = 0.8 (80% parallelisable), p = 4 processors: "
        "S = 1 / (0.2 + 0.8/4) = 1 / (0.2 + 0.2) = 1/0.4 = 2.5x."
    ),
    tier=4,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Amdahl's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Amdahl%27s_law",
    prerequisites=["division"],
))
