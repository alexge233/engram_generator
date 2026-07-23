"""Knowledge atoms for CS, math, and applied science generators (batch 3).

Covers: crypto_ext, cryptanalysis, cryptography, automata_ext, automata_deep,
coding_theory, networking, networking_ext, computer_architecture,
digital_electronics, music_theory, recursion_ext, spatial_ext, spatial_deep,
diffgeo_ext, diffeq_ext, trigonometry_ext, sequences_ext, measure_ext,
persistent_homology, model_theory, category_ext, convex_optimization,
numerical_linalg, numerical_ext2.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Cryptography ext (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="dsa_sign",
    content=(
        "The Digital Signature Algorithm (DSA) signs a message hash using a "
        "private key x. Choose random k, compute r = (g^k mod p) mod q, "
        "s = k^{-1} * (H(m) + x*r) mod q. The signature is (r, s). "
        "Verification checks g^{H(m)*w} * y^{r*w} mod p mod q == r, "
        "where w = s^{-1} mod q."
    ),
    example=(
        "p=23, q=11, g=4, x=7, k=3. r = (4^3 mod 23) mod 11 = 18 mod 11 = 7. "
        "For H(m) = 5: s = 3^{-1}*(5+7*7) mod 11 = 4*(5+49) mod 11 = 4*54 mod 11 = 216 mod 11 = 7."
    ),
    tier=6,
    domain="cryptography",
    source="Wikipedia contributors, 'Digital Signature Algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Digital_Signature_Algorithm",
    prerequisites=["modpow", "modinv"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="shamir_secret_share",
    content=(
        "Shamir's Secret Sharing splits a secret S into n shares such that "
        "any k shares can reconstruct S, but k-1 cannot. A random polynomial "
        "f(x) of degree k-1 is created with f(0) = S. Shares are (i, f(i)) "
        "for i = 1..n. Reconstruction uses Lagrange interpolation at x = 0."
    ),
    example=(
        "Secret S=42, k=2 (threshold), polynomial f(x)=42+3x (mod 97). "
        "Shares: (1,45), (2,48), (3,51). Any 2 shares reconstruct S=42."
    ),
    tier=5,
    domain="cryptography",
    source="Wikipedia contributors, 'Shamir's Secret Sharing', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="concept",
    name="commitment_scheme",
    content=(
        "A cryptographic commitment scheme lets a party commit to a value "
        "without revealing it, then later reveal it verifiably. Pedersen "
        "commitment: C = g^m * h^r mod p, where m is the message, r is random. "
        "Properties: hiding (C reveals nothing about m) and binding "
        "(cannot open to different m)."
    ),
    example=(
        "g=4, h=9, p=23, m=7, r=3. C = 4^7 * 9^3 mod 23 = 16384*729 mod 23 "
        "= 11943936 mod 23 = 2."
    ),
    tier=6,
    domain="cryptography",
    source="Wikipedia contributors, 'Commitment scheme', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Commitment_scheme",
    prerequisites=["modpow"],
))

register_atom(Atom(
    atom_type="concept",
    name="zero_knowledge_basic",
    content=(
        "A zero-knowledge proof lets a prover convince a verifier of a "
        "statement's truth without revealing any information beyond the "
        "statement's validity. Properties: completeness (honest prover "
        "convinces), soundness (cheating prover caught), zero-knowledge "
        "(verifier learns nothing else). Example: graph colouring protocol."
    ),
    example=(
        "Prover knows a 3-colouring of a graph. Commits to a random permutation "
        "of colours. Verifier picks an edge; prover reveals those two vertices' "
        "colours. If different, verifier accepts. Repeat to gain confidence."
    ),
    tier=6,
    domain="cryptography",
    source="Wikipedia contributors, 'Zero-knowledge proof', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Zero-knowledge_proof",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="merkle_tree",
    content=(
        "A Merkle tree is a binary hash tree where each leaf is a hash of a "
        "data block and each internal node is the hash of its children. "
        "The root hash authenticates all data. Proof of inclusion for a leaf "
        "requires O(log n) sibling hashes. Used in blockchains and certificate "
        "transparency."
    ),
    example=(
        "4 blocks: H0=H(B0), H1=H(B1), H2=H(B2), H3=H(B3). "
        "H01=H(H0||H1), H23=H(H2||H3). Root=H(H01||H23). "
        "Proof for B1: provide H0 and H23."
    ),
    tier=5,
    domain="cryptography",
    source="Wikipedia contributors, 'Merkle tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Merkle_tree",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="stream_cipher",
    content=(
        "A stream cipher encrypts plaintext one bit/byte at a time by XORing "
        "with a pseudorandom keystream. C_i = P_i XOR K_i. The keystream is "
        "generated from a seed key using a PRNG (e.g. LFSR, RC4, ChaCha20). "
        "Security depends on keystream unpredictability."
    ),
    example=(
        "Keystream: [0x3A, 0x7F, 0x12]. Plaintext: [0x48, 0x65, 0x6C] ('Hel'). "
        "Ciphertext: [0x48^0x3A, 0x65^0x7F, 0x6C^0x12] = [0x72, 0x1A, 0x7E]."
    ),
    tier=5,
    domain="cryptography",
    source="Wikipedia contributors, 'Stream cipher', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stream_cipher",
    prerequisites=["otp_encrypt"],
))

register_atom(Atom(
    atom_type="concept",
    name="block_cipher_modes",
    content=(
        "Block cipher modes of operation define how to repeatedly apply a "
        "block cipher to multiple blocks. ECB: each block encrypted independently "
        "(insecure, patterns visible). CBC: each block XORed with previous "
        "ciphertext (needs IV). CTR: encrypts counter values, XORs with "
        "plaintext (parallelisable). GCM adds authentication."
    ),
    example=(
        "AES-CBC: C_0 = E_K(P_0 XOR IV), C_1 = E_K(P_1 XOR C_0), ... "
        "Decryption: P_0 = D_K(C_0) XOR IV."
    ),
    tier=5,
    domain="cryptography",
    source="Wikipedia contributors, 'Block cipher mode of operation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation",
    prerequisites=["feistel_round"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="aes_mixcolumn",
    content=(
        "MixColumns is a step in AES that multiplies each column of the state "
        "by a fixed matrix in GF(2^8). The matrix is "
        "[[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]. Multiplication in GF(2^8) "
        "uses the irreducible polynomial x^8+x^4+x^3+x+1."
    ),
    example=(
        "Input column [0xDB, 0x13, 0x53, 0x45]. "
        "After MixColumns: [0x8E, 0x4D, 0xA1, 0xBC]."
    ),
    tier=5,
    domain="cryptography",
    source="Wikipedia contributors, 'Rijndael MixColumns', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rijndael_MixColumns",
    prerequisites=["matrix_multiply"],
))

# ---------------------------------------------------------------------------
# Cryptanalysis (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="method",
    name="frequency_analysis",
    content=(
        "Frequency analysis exploits the non-uniform distribution of letters "
        "in natural language to break substitution ciphers. In English, 'E' is "
        "most common (~12.7%), followed by T (~9.1%), A (~8.2%). Comparing "
        "ciphertext frequencies to expected frequencies reveals the key."
    ),
    example=(
        "Ciphertext most common letter: 'X' (13%). Likely maps to 'E'. "
        "If Caesar cipher: shift = ord('X') - ord('E') = 88-69 = 19."
    ),
    tier=5,
    domain="cryptanalysis",
    source="Wikipedia contributors, 'Frequency analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Frequency_analysis",
    prerequisites=["caesar"],
))

register_atom(Atom(
    atom_type="method",
    name="known_plaintext",
    content=(
        "A known-plaintext attack uses pairs of known plaintext and "
        "corresponding ciphertext to deduce the key. For XOR-based ciphers: "
        "K = P XOR C. For linear ciphers: if C = A*P + B, two pairs yield "
        "A and B. Applicable when some message content is predictable "
        "(headers, signatures)."
    ),
    example=(
        "XOR cipher: known P='HELLO' (0x48,0x45,0x4C,0x4C,0x4F), "
        "C=(0x7A,0x77,0x7E,0x7E,0x7D). K = P XOR C = (0x32,0x32,0x32,0x32,0x32) = '22222'."
    ),
    tier=5,
    domain="cryptanalysis",
    source="Wikipedia contributors, 'Known-plaintext attack', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Known-plaintext_attack",
    prerequisites=["otp_encrypt"],
))

register_atom(Atom(
    atom_type="method",
    name="meet_in_middle",
    content=(
        "Meet-in-the-middle attack reduces the cost of attacking double "
        "encryption from O(2^(2n)) to O(2^(n+1)) in time and O(2^n) space. "
        "Encrypt P with all possible K1, store results. Decrypt C with all "
        "possible K2, find matches. This is why Double-DES is insecure "
        "(only 57-bit effective security instead of 112)."
    ),
    example=(
        "Double-DES: 2^56 encryptions + 2^56 decryptions + sorting = ~2^57 work. "
        "Much less than brute-forcing 2^112 key pairs."
    ),
    tier=5,
    domain="cryptanalysis",
    source="Wikipedia contributors, 'Meet-in-the-middle attack', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Meet-in-the-middle_attack",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="birthday_attack",
    content=(
        "The birthday attack exploits the birthday paradox to find hash "
        "collisions. For a hash of n bits, a collision is expected after "
        "~2^(n/2) random inputs (not 2^n). This sets the minimum hash size: "
        "128-bit hash has only 64-bit collision resistance. SHA-256 provides "
        "128-bit collision resistance."
    ),
    example=(
        "16-bit hash: collision expected after ~2^8 = 256 trials. "
        "128-bit hash: collision after ~2^64 ~ 1.8e19 trials."
    ),
    tier=5,
    domain="cryptanalysis",
    source="Wikipedia contributors, 'Birthday attack', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Birthday_attack",
    prerequisites=["exponentiation"],
))

# ---------------------------------------------------------------------------
# Networking (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="concept",
    name="tcp_window",
    content=(
        "The TCP sliding window controls flow: the receiver advertises a "
        "window size (bytes it can buffer). The sender can have at most "
        "window_size bytes in flight. Throughput <= window_size / RTT. "
        "Window scaling option allows windows up to 1 GB."
    ),
    example=(
        "Window = 64 KB, RTT = 100 ms. Max throughput = 65536 / 0.1 "
        "= 655360 bytes/s = 5.24 Mbps."
    ),
    tier=5,
    domain="networking",
    source="Wikipedia contributors, 'TCP window scale option', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/TCP_window_scale_option",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="concept",
    name="routing_table",
    content=(
        "A routing table maps destination networks to next-hop addresses "
        "and interfaces. Longest prefix match: the most specific route "
        "(longest subnet mask) is selected. Default route (0.0.0.0/0) is "
        "used when no specific match exists."
    ),
    example=(
        "Routes: 10.0.0.0/8 -> gw1, 10.1.0.0/16 -> gw2, 0.0.0.0/0 -> gw3. "
        "Packet to 10.1.2.3: matches /16 (longest prefix) -> gw2."
    ),
    tier=4,
    domain="networking",
    source="Wikipedia contributors, 'Routing table', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Routing_table",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="crc_check",
    content=(
        "Cyclic Redundancy Check (CRC) detects errors by treating data as a "
        "polynomial and computing the remainder when divided by a generator "
        "polynomial. CRC-32 uses generator 0x04C11DB7. The sender appends "
        "the CRC; the receiver divides and checks for zero remainder."
    ),
    example=(
        "Data: 1101, Generator: 1011 (CRC-3). Append 3 zeros: 1101000. "
        "XOR division gives remainder 001. Transmit: 1101001."
    ),
    tier=5,
    domain="networking",
    source="Wikipedia contributors, 'Cyclic redundancy check', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cyclic_redundancy_check",
    prerequisites=["polynomial_division"],
))

register_atom(Atom(
    atom_type="formula",
    name="network_delay",
    content=(
        "Total packet delay = propagation + transmission + queuing + processing. "
        "Propagation delay = distance / speed (~2e8 m/s in fibre). "
        "Transmission delay = packet_size / bandwidth. "
        "Queuing delay depends on traffic intensity rho = arrival_rate * packet_size / bandwidth."
    ),
    example=(
        "1500 bytes over 100 Mbps, 1000 km fibre. "
        "Transmission = 12000 bits / 1e8 = 0.12 ms. "
        "Propagation = 1e6 / 2e8 = 5 ms. Total ~ 5.12 ms."
    ),
    tier=5,
    domain="networking",
    source="Wikipedia contributors, 'Network delay', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Network_delay",
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Networking ext (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="ip_subnetting",
    content=(
        "IP subnetting divides a network into smaller subnets using a subnet "
        "mask. Network address = IP AND mask. Broadcast = IP OR (NOT mask). "
        "Host range: network+1 to broadcast-1. A /24 gives 254 hosts, "
        "/25 gives 126, /26 gives 62."
    ),
    example=(
        "IP: 192.168.1.130/26. Mask: 255.255.255.192. "
        "Network: 192.168.1.128. Broadcast: 192.168.1.191. "
        "Hosts: 192.168.1.129 - 192.168.1.190 (62 hosts)."
    ),
    tier=5,
    domain="networking",
    source="Wikipedia contributors, 'Subnetwork', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Subnetwork",
    prerequisites=["binary_arithmetic"],
))

register_atom(Atom(
    atom_type="concept",
    name="arp_resolution",
    content=(
        "ARP (Address Resolution Protocol) maps IP addresses to MAC addresses "
        "on a local network. A host broadcasts an ARP request ('who has IP X?'). "
        "The owner responds with its MAC. Results are cached in the ARP table. "
        "ARP operates at Layer 2."
    ),
    example=(
        "Host A (IP 10.0.0.1) wants to reach 10.0.0.2. Broadcasts ARP request. "
        "Host B (10.0.0.2, MAC aa:bb:cc:dd:ee:ff) replies. "
        "A caches: 10.0.0.2 -> aa:bb:cc:dd:ee:ff."
    ),
    tier=5,
    domain="networking",
    source="Wikipedia contributors, 'Address Resolution Protocol', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Address_Resolution_Protocol",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="concept",
    name="dns_resolution",
    content=(
        "DNS resolves domain names to IP addresses through a hierarchical "
        "system. Resolution steps: local cache -> recursive resolver -> "
        "root server -> TLD server -> authoritative server. Record types: "
        "A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), NS (nameserver)."
    ),
    example=(
        "Query: example.com. Root server -> .com TLD -> example.com authoritative. "
        "Returns A record: 93.184.216.34. Cached with TTL."
    ),
    tier=5,
    domain="networking",
    source="Wikipedia contributors, 'Domain Name System', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Domain_Name_System",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="tcp_congestion",
    content=(
        "TCP congestion control adjusts sending rate to avoid network overload. "
        "Slow start: cwnd doubles each RTT until ssthresh. Congestion avoidance: "
        "cwnd increases by 1 MSS per RTT. On loss (timeout): ssthresh = cwnd/2, "
        "cwnd = 1. On triple duplicate ACK (fast retransmit): cwnd halved."
    ),
    example=(
        "Initial cwnd=1 MSS, ssthresh=16. After 4 RTTs in slow start: "
        "cwnd = 1, 2, 4, 8, 16. At cwnd=16 (= ssthresh): switch to "
        "congestion avoidance: 17, 18, 19..."
    ),
    tier=5,
    domain="networking",
    source="Wikipedia contributors, 'TCP congestion control', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/TCP_congestion_control",
    prerequisites=["tcp_window"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="checksum_compute",
    content=(
        "Internet checksum (RFC 1071): split data into 16-bit words, sum with "
        "ones-complement arithmetic (carry wraps around), take ones-complement "
        "of sum. Used in IP, TCP, UDP headers. Verification: sum all words "
        "including checksum; result should be 0xFFFF."
    ),
    example=(
        "Words: 0x4500, 0x0073, 0x0000. Sum = 0x4573. "
        "Ones-complement: 0xBA8C. To verify: 0x4500+0x0073+0x0000+0xBA8C = 0xFFFF."
    ),
    tier=5,
    domain="networking",
    source="Wikipedia contributors, 'IPv4 header checksum', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/IPv4_header_checksum",
    prerequisites=["binary_arithmetic"],
))

register_atom(Atom(
    atom_type="concept",
    name="sliding_window",
    content=(
        "Sliding window protocols (Go-Back-N, Selective Repeat) allow multiple "
        "packets in flight. Sender window: frames that can be sent without ACK. "
        "Go-Back-N: receiver only accepts in-order; on error retransmits "
        "all from lost frame. Selective Repeat: buffers out-of-order; "
        "retransmits only lost frames."
    ),
    example=(
        "Window size W=4, sequence numbers 0-7. Frames 0,1,2,3 sent. "
        "ACK 0,1 received: window slides to 2,3,4,5."
    ),
    tier=5,
    domain="networking",
    source="Wikipedia contributors, 'Sliding window protocol', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Sliding_window_protocol",
    prerequisites=["tcp_window"],
))

# ---------------------------------------------------------------------------
# Computer architecture (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="pipeline_throughput",
    content=(
        "An n-stage pipeline processes one instruction per clock cycle "
        "(steady state). Speedup = n (ideal). Throughput = f (clock frequency). "
        "Hazards reduce performance: data hazards (forwarding/stalling), "
        "control hazards (branch prediction). CPI = 1 + stall_cycles_per_instruction."
    ),
    example=(
        "5-stage pipeline, 1 GHz clock, 20% branch misprediction with 2-cycle penalty. "
        "CPI = 1 + 0.2*2 = 1.4. Throughput = 1e9/1.4 = 714 MIPS."
    ),
    tier=5,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Instruction pipelining', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Instruction_pipelining",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="cache_hit_ratio",
    content=(
        "Cache hit ratio h = hits / (hits + misses). Average memory access "
        "time AMAT = h*t_cache + (1-h)*t_memory. For multi-level caches: "
        "AMAT = t_L1 + (1-h_L1)*(t_L2 + (1-h_L2)*t_mem)."
    ),
    example=(
        "h = 0.95, t_cache = 1 ns, t_memory = 100 ns. "
        "AMAT = 0.95*1 + 0.05*100 = 0.95 + 5 = 5.95 ns."
    ),
    tier=5,
    domain="computer_architecture",
    source="Wikipedia contributors, 'CPU cache', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/CPU_cache#Cache_performance",
    prerequisites=["weighted_sum"],
))

register_atom(Atom(
    atom_type="concept",
    name="branch_prediction",
    content=(
        "Branch prediction guesses the outcome of conditional branches before "
        "they execute. Static: predict not-taken or backward-taken. Dynamic: "
        "1-bit (last outcome), 2-bit saturating counter (needs 2 mispredictions "
        "to change). BTB (Branch Target Buffer) caches branch destinations."
    ),
    example=(
        "2-bit predictor, initial state 'strongly taken' (11). "
        "Branch not taken: state -> 10 (weakly taken), still predicts taken. "
        "Not taken again: state -> 01, now predicts not-taken."
    ),
    tier=5,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Branch predictor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Branch_predictor",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="concept",
    name="instruction_scheduling",
    content=(
        "Instruction scheduling reorders instructions to avoid pipeline stalls "
        "while maintaining correctness (data dependencies). List scheduling "
        "assigns priorities based on critical path length. Out-of-order "
        "execution uses a reservation station (Tomasulo's algorithm) to "
        "dynamically schedule."
    ),
    example=(
        "Instructions: ADD R1,R2,R3; MUL R4,R1,R5 (RAW hazard on R1). "
        "Insert independent instruction between them to fill the stall cycle."
    ),
    tier=5,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Instruction scheduling', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Instruction_scheduling",
    prerequisites=["pipeline_throughput"],
))

register_atom(Atom(
    atom_type="concept",
    name="memory_hierarchy",
    content=(
        "The memory hierarchy trades off speed, size, and cost: "
        "registers (< 1 ns, bytes) > L1 cache (1 ns, KB) > L2 (5 ns, MB) > "
        "L3 (20 ns, MB) > DRAM (100 ns, GB) > SSD (100 us, TB) > HDD (10 ms, TB). "
        "Temporal and spatial locality make caching effective."
    ),
    example=(
        "L1 hit rate 95%, L2 hit rate 80% of L1 misses. "
        "Miss rate to DRAM = 5% * 20% = 1%."
    ),
    tier=5,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Memory hierarchy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Memory_hierarchy",
    prerequisites=["cache_hit_ratio"],
))

register_atom(Atom(
    atom_type="formula",
    name="amdahl_speedup",
    content=(
        "Amdahl's law gives the maximum speedup when parallelising a fraction "
        "p of a program with n processors: S = 1 / ((1-p) + p/n). Even with "
        "infinite processors, S <= 1/(1-p). Gustafson's law considers scaling "
        "the problem size: S = (1-p) + p*n."
    ),
    example=(
        "90% parallel (p=0.9), 8 processors. "
        "S = 1/(0.1 + 0.9/8) = 1/(0.1 + 0.1125) = 1/0.2125 = 4.71x."
    ),
    tier=5,
    domain="computer_architecture",
    source="Wikipedia contributors, 'Amdahl's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Amdahl%27s_law",
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Music theory (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="concept",
    name="interval_identify",
    content=(
        "A musical interval is the distance between two pitches measured in "
        "semitones. Unison=0, minor 2nd=1, major 2nd=2, minor 3rd=3, "
        "major 3rd=4, perfect 4th=5, tritone=6, perfect 5th=7, "
        "minor 6th=8, major 6th=9, minor 7th=10, major 7th=11, octave=12."
    ),
    example=(
        "C to E: 4 semitones = major 3rd. C to Ab: 8 semitones = minor 6th."
    ),
    tier=4,
    domain="music_theory",
    source="Wikipedia contributors, 'Interval (music)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Interval_(music)",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="concept",
    name="chord_construct",
    content=(
        "Chords are built by stacking intervals. Major triad: root + major 3rd "
        "(4 semitones) + perfect 5th (7). Minor: root + minor 3rd (3) + P5 (7). "
        "Diminished: 3 + 6. Augmented: 4 + 8. Seventh chords add another third. "
        "Inversions rearrange the notes."
    ),
    example=(
        "C major: C-E-G (0,4,7 semitones). A minor: A-C-E (0,3,7). "
        "G7: G-B-D-F (0,4,7,10)."
    ),
    tier=4,
    domain="music_theory",
    source="Wikipedia contributors, 'Chord (music)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chord_(music)",
    prerequisites=["interval_identify"],
))

register_atom(Atom(
    atom_type="concept",
    name="chord_progression",
    content=(
        "A chord progression is a sequence of chords. Roman numeral analysis: "
        "I=tonic, IV=subdominant, V=dominant, vi=relative minor. Common "
        "progressions: I-IV-V-I (blues), I-V-vi-IV (pop), ii-V-I (jazz). "
        "Voice leading connects chords with smooth motion."
    ),
    example=(
        "Key of C major: I-V-vi-IV = C-G-Am-F."
    ),
    tier=5,
    domain="music_theory",
    source="Wikipedia contributors, 'Chord progression', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chord_progression",
    prerequisites=["chord_construct"],
))

register_atom(Atom(
    atom_type="concept",
    name="voice_leading",
    content=(
        "Voice leading governs how individual voices (parts) move between "
        "chords. Rules: prefer stepwise motion, avoid parallel 5ths and "
        "octaves, keep common tones, resolve leading tones up and 7ths down. "
        "Smooth voice leading minimises total voice movement."
    ),
    example=(
        "C major to G major: C stays (common tone), E moves to D (step down), "
        "G stays (common tone), add B."
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
        "In equal temperament, the frequency ratio between adjacent semitones "
        "is 2^(1/12) ~ 1.0595. The frequency n semitones above A4 (440 Hz) "
        "is f = 440 * 2^(n/12). Cents: 100 cents = 1 semitone, "
        "c = 1200 * log2(f2/f1)."
    ),
    example=(
        "Middle C (C4) is 9 semitones below A4. f = 440 * 2^(-9/12) "
        "= 440 * 0.5946 = 261.6 Hz."
    ),
    tier=4,
    domain="music_theory",
    source="Wikipedia contributors, 'Equal temperament', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Equal_temperament",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="concept",
    name="rhythm_subdivision",
    content=(
        "Rhythm subdivision divides beats into smaller units. A whole note = "
        "4 beats, half = 2, quarter = 1, eighth = 1/2, sixteenth = 1/4. "
        "Dotted notes add half their value. Triplets divide a beat into 3 "
        "equal parts. Time signatures: 4/4 (common), 3/4 (waltz), 6/8 (compound)."
    ),
    example=(
        "4/4 time: one bar = 4 quarter notes = 8 eighth notes = 16 sixteenths. "
        "Dotted quarter = 1.5 beats."
    ),
    tier=4,
    domain="music_theory",
    source="Wikipedia contributors, 'Note value', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Note_value",
    prerequisites=["fraction_arithmetic"],
))

# ---------------------------------------------------------------------------
# Coding theory (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="linear_code",
    content=(
        "A linear code C(n,k) encodes k information bits into n-bit codewords "
        "using generator matrix G: c = m*G. Parity check matrix H satisfies "
        "H*c^T = 0 for valid codewords. Minimum distance d determines error "
        "correction: corrects floor((d-1)/2) errors."
    ),
    example=(
        "Hamming(7,4): n=7, k=4, d=3. Corrects 1 error. "
        "G = [I_4 | P], H = [-P^T | I_3]. Rate = 4/7 = 0.571."
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
        "Syndrome decoding computes s = H*r^T for received word r. If s = 0, "
        "no error. Otherwise, s matches a column of H, identifying the error "
        "position. For single-error correction: flip the bit at that position. "
        "Complexity is O(n-k) instead of comparing all codewords."
    ),
    example=(
        "Hamming(7,4): received r = [1,0,1,1,0,1,1]. "
        "s = H*r^T = [1,0,1]. Column 5 of H matches. Error at bit 5. "
        "Corrected: [1,0,1,1,1,1,1]."
    ),
    tier=5,
    domain="coding_theory",
    source="Wikipedia contributors, 'Decoding methods', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Decoding_methods#Syndrome_decoding",
    prerequisites=["linear_code"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="bch_encode",
    content=(
        "BCH codes are a class of cyclic error-correcting codes. A BCH(n,k,t) "
        "code over GF(2) corrects up to t errors. The generator polynomial "
        "g(x) is the LCM of minimal polynomials of alpha, alpha^2, ..., alpha^(2t). "
        "Encoding: c(x) = m(x)*x^(n-k) + (m(x)*x^(n-k) mod g(x))."
    ),
    example=(
        "BCH(15,7,2): corrects 2 errors, g(x) has degree 8. "
        "Message 1000000 -> codeword 100000010100110."
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
        "Reed-Solomon codes operate on symbols (not bits) over GF(2^m). "
        "RS(n,k) with symbols of m bits corrects up to t = (n-k)/2 symbol "
        "errors. Used in CDs (RS(255,223) over GF(2^8)), QR codes, and "
        "deep-space communication. Decoding uses Berlekamp-Massey algorithm."
    ),
    example=(
        "RS(255,223) over GF(2^8): 223 data symbols, 32 parity symbols. "
        "Corrects up to 16 symbol errors."
    ),
    tier=6,
    domain="coding_theory",
    source="Wikipedia contributors, 'Reed-Solomon error correction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction",
    prerequisites=["polynomial_multiply"],
))

register_atom(Atom(
    atom_type="formula",
    name="code_parameters",
    content=(
        "Key parameters of an error-correcting code: rate R = k/n (efficiency), "
        "minimum distance d (error correction capability), "
        "Singleton bound: d <= n - k + 1 (MDS codes achieve equality). "
        "Hamming bound: sum_{i=0}^{t} C(n,i) <= 2^(n-k), t = floor((d-1)/2)."
    ),
    example=(
        "Hamming(7,4): R = 4/7 = 0.571, d = 3, t = 1. "
        "Hamming bound: C(7,0)+C(7,1) = 1+7 = 8 = 2^3 = 2^(7-4). Perfect code."
    ),
    tier=5,
    domain="coding_theory",
    source="Wikipedia contributors, 'Hamming bound', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hamming_bound",
    prerequisites=["binomial"],
))

register_atom(Atom(
    atom_type="concept",
    name="turbo_code_interleave",
    content=(
        "Turbo codes use two parallel convolutional encoders separated by an "
        "interleaver. The interleaver permutes the input bits before the second "
        "encoder, creating independent parity. Iterative decoding (BCJR/MAP) "
        "exchanges soft information between decoders. Near Shannon limit performance."
    ),
    example=(
        "Rate 1/3 turbo code: systematic bits + parity from encoder 1 + "
        "parity from encoder 2 (after interleaving). "
        "6 iterations of decoding typically suffice."
    ),
    tier=6,
    domain="coding_theory",
    source="Wikipedia contributors, 'Turbo code', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Turbo_code",
    prerequisites=["linear_code"],
))

# ---------------------------------------------------------------------------
# Automata ext (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="concept",
    name="mealy_machine",
    content=(
        "A Mealy machine is a finite state machine where outputs depend on "
        "both the current state and input: output = lambda(state, input). "
        "Transition function: delta(state, input) -> next_state. "
        "Output is associated with transitions, not states."
    ),
    example=(
        "States {S0,S1}, input {0,1}. delta(S0,0)=S0 output 0, "
        "delta(S0,1)=S1 output 1, delta(S1,0)=S0 output 1, delta(S1,1)=S1 output 0. "
        "Input 101: output 110."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Mealy machine', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mealy_machine",
    prerequisites=["dfa_accept"],
))

register_atom(Atom(
    atom_type="concept",
    name="moore_machine",
    content=(
        "A Moore machine is a finite state machine where output depends only "
        "on the current state: output = lambda(state). Transition function: "
        "delta(state, input) -> next_state. Equivalent to Mealy machines "
        "but may need more states."
    ),
    example=(
        "States {S0(out=0), S1(out=1)}. delta(S0,1)=S1, delta(S1,0)=S0. "
        "Input 110: states S0->S1->S1->S0, outputs 0,1,1,0."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Moore machine', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Moore_machine",
    prerequisites=["dfa_accept"],
))

register_atom(Atom(
    atom_type="concept",
    name="transducer",
    content=(
        "A finite-state transducer (FST) is a finite automaton with both input "
        "and output tapes. It defines a relation between input and output strings. "
        "Mealy and Moore machines are special cases. FSTs are used in NLP "
        "(morphological analysis), speech recognition, and compiler lexers."
    ),
    example=(
        "Binary-to-Gray code transducer: input 0110, output 0101. "
        "Rule: first output = first input; subsequent outputs = input XOR previous input."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Finite-state transducer', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Finite-state_transducer",
    prerequisites=["mealy_machine"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="dfa_minimization",
    content=(
        "DFA minimisation finds the smallest DFA accepting the same language. "
        "Hopcroft's algorithm partitions states by distinguishability: "
        "two states are equivalent if no string separates them. "
        "Start with {accepting, non-accepting}, refine by checking transitions. "
        "Complexity: O(n log n)."
    ),
    example=(
        "DFA with states {A,B,C,D}. A,C are accepting. "
        "If delta(A,0) = delta(C,0) and delta(A,1) = delta(C,1), "
        "then A and C are equivalent; merge into one state."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'DFA minimization', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/DFA_minimization",
    prerequisites=["dfa_accept"],
))

register_atom(Atom(
    atom_type="theorem",
    name="pumping_lemma_cfl",
    content=(
        "The pumping lemma for context-free languages: for every CFL L, "
        "there exists p such that any s in L with |s| >= p can be written as "
        "s = uvxyz where |vy| >= 1, |vxy| <= p, and uv^i xy^i z is in L "
        "for all i >= 0. Used to prove languages are NOT context-free."
    ),
    example=(
        "L = {a^n b^n c^n}: pump v and y. If v=a^j y=b^j, then pumping "
        "gives more a's and b's but not c's. Not CFL."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Pumping lemma for context-free languages', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pumping_lemma_for_context-free_languages",
    prerequisites=["cfg_derivation"],
))

register_atom(Atom(
    atom_type="concept",
    name="two_stack_pda",
    content=(
        "A PDA with two stacks is equivalent to a Turing machine. One stack "
        "simulates the tape left of the head, the other the right. This shows "
        "that adding a second stack to a PDA increases computational power "
        "beyond context-free languages to recursively enumerable."
    ),
    example=(
        "To recognise {a^n b^n c^n}: push a's on stack 1. For each b, "
        "pop stack 1 and push stack 2. For each c, pop stack 2. "
        "Accept if both stacks empty."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Pushdown automaton', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pushdown_automaton#Equivalence_with_Turing_machines",
    prerequisites=["pushdown_simulate"],
))

# ---------------------------------------------------------------------------
# Automata deep (tier 5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="dfa_complement",
    content=(
        "The complement of a DFA is obtained by swapping accepting and "
        "non-accepting states. If L(M) = L, then L(M') = Sigma* - L. "
        "The DFA must be complete (transitions defined for all state-input pairs). "
        "Add a dead/trap state if needed."
    ),
    example=(
        "DFA accepting strings ending in 0: states {q0(non-accept), q1(accept)}. "
        "Complement: q0 becomes accept, q1 becomes non-accept. "
        "Accepts strings NOT ending in 0."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Complement (set theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Complement_(complexity)#Closure_properties",
    prerequisites=["dfa_accept"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="dfa_product",
    content=(
        "The product construction builds a DFA for the intersection (or union) "
        "of two DFAs. States are pairs (q1, q2). Transitions: "
        "delta((q1,q2), a) = (delta1(q1,a), delta2(q2,a)). Accept states: "
        "both accepting (intersection) or either accepting (union)."
    ),
    example=(
        "M1 accepts multiples of 2, M2 accepts multiples of 3. "
        "Product (intersection) accepts multiples of 6."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Product automaton', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Product_construction_(automata_theory)",
    prerequisites=["dfa_accept"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="regex_to_dfa_direct",
    content=(
        "Direct regex-to-DFA construction: compute firstpos, lastpos, and "
        "followpos for each node in the syntax tree. States are sets of "
        "positions. Start state = firstpos(root). Transitions follow the "
        "followpos relation. No intermediate NFA is needed."
    ),
    example=(
        "Regex (a|b)*abb. Augmented: (a|b)*abb#. Positions 1-6. "
        "Start state = {1,2,3}. Build transitions by followpos."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Thompson's construction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Thompson%27s_construction",
    prerequisites=["nfa_to_dfa"],
))

register_atom(Atom(
    atom_type="concept",
    name="language_operations",
    content=(
        "Regular languages are closed under union, intersection, complement, "
        "concatenation, and Kleene star. If L1 and L2 are regular, so are "
        "L1 union L2, L1 intersect L2, complement(L1), L1.L2, and L1*. "
        "Context-free languages are closed under union, concatenation, and star, "
        "but NOT intersection or complement."
    ),
    example=(
        "L1 = {a^n b^n}, L2 = {b^n c^n}. Both CFL. "
        "L1 intersect L2 = {a^n b^n c^n}, which is NOT CFL."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Regular language', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Regular_language#Closure_properties",
    prerequisites=["dfa_accept"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="state_equivalence",
    content=(
        "Two DFA states p and q are equivalent (indistinguishable) if for "
        "every string w, delta(p,w) is accepting iff delta(q,w) is accepting. "
        "Table-filling algorithm: mark pairs where one is accepting and one "
        "isn't. Iterate: mark (p,q) if delta(p,a) and delta(q,a) are marked "
        "for some input a. Unmarked pairs are equivalent."
    ),
    example=(
        "States {A,B,C}. A accepts, B,C don't. (A,B) and (A,C) are marked. "
        "If delta(B,0)=delta(C,0) and delta(B,1)=delta(C,1), B and C are equivalent."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Myhill-Nerode theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Myhill%E2%80%93Nerode_theorem",
    prerequisites=["dfa_minimization"],
))

register_atom(Atom(
    atom_type="theorem",
    name="myhill_nerode",
    content=(
        "The Myhill-Nerode theorem characterises regular languages: L is regular "
        "iff the number of equivalence classes of the right-invariant relation "
        "~_L is finite. x ~_L y iff for all z: xz in L iff yz in L. "
        "The number of classes equals the number of states in the minimal DFA."
    ),
    example=(
        "L = {strings with even number of a's}. Two classes: "
        "[even] and [odd] (based on number of a's seen). "
        "Finite classes -> regular. Minimal DFA has 2 states."
    ),
    tier=5,
    domain="automata",
    source="Wikipedia contributors, 'Myhill-Nerode theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Myhill%E2%80%93Nerode_theorem",
    prerequisites=["state_equivalence"],
))

# ---------------------------------------------------------------------------
# Remaining modules: brief atoms
# (recursion_ext, spatial_ext, spatial_deep, etc.)
# ---------------------------------------------------------------------------

# Recursion ext (tier 4)

register_atom(Atom(
    atom_type="algorithm", name="tower_of_hanoi",
    content="Tower of Hanoi: move n disks from source to target using auxiliary peg. Recursive: move n-1 to aux, move largest to target, move n-1 from aux to target. Minimum moves = 2^n - 1.",
    example="n=3: 2^3-1 = 7 moves. Sequence: A->C, A->B, C->B, A->C, B->A, B->C, A->C.",
    tier=4, domain="algorithms",
    source="Wikipedia contributors, 'Tower of Hanoi', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tower_of_Hanoi",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="algorithm", name="recursive_power",
    content="Fast exponentiation by squaring: pow(b,n) = pow(b,n/2)^2 if n even, b*pow(b,n-1) if odd. Reduces O(n) multiplications to O(log n). Base case: pow(b,0) = 1.",
    example="3^5: 3^5 = 3*3^4 = 3*(3^2)^2 = 3*(9)^2 = 3*81 = 243. 4 multiplications instead of 5.",
    tier=4, domain="algorithms",
    source="Wikipedia contributors, 'Exponentiation by squaring', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exponentiation_by_squaring",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="algorithm", name="recursive_gcd",
    content="Euclidean algorithm: gcd(a,b) = gcd(b, a mod b), base case gcd(a,0) = a. Each step reduces the problem size by at least half. Complexity: O(log(min(a,b))).",
    example="gcd(48,18): gcd(48,18) = gcd(18,12) = gcd(12,6) = gcd(6,0) = 6.",
    tier=4, domain="algorithms",
    source="Wikipedia contributors, 'Euclidean algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euclidean_algorithm",
    prerequisites=["gcd"],
))

register_atom(Atom(
    atom_type="algorithm", name="recursive_binary_search",
    content="Binary search recursively halves the search space: compare target with middle element. If less, search left half; if greater, search right half. Complexity: O(log n). Requires sorted input.",
    example="Search for 7 in [1,3,5,7,9]: mid=5 (less), search right [7,9]: mid=7 (found). 2 comparisons.",
    tier=4, domain="algorithms",
    source="Wikipedia contributors, 'Binary search algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Binary_search_algorithm",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm", name="recursive_sum",
    content="Recursive sum: sum(arr, n) = arr[n-1] + sum(arr, n-1), base case sum(arr, 0) = 0. Demonstrates basic recursion with accumulation. Tail-recursive version uses an accumulator parameter.",
    example="sum([3,1,4,1,5], 5) = 5 + sum([3,1,4,1], 4) = ... = 3+1+4+1+5 = 14.",
    tier=3, domain="algorithms",
    source="Wikipedia contributors, 'Recursion (computer science)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Recursion_(computer_science)",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="algorithm", name="recursive_permutations",
    content="Generate all permutations recursively: for each element, place it first and permute the rest. n! total permutations. Heap's algorithm generates all permutations with O(1) swaps between consecutive outputs.",
    example="Permutations of [1,2,3]: [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]. 3! = 6 total.",
    tier=4, domain="algorithms",
    source="Wikipedia contributors, 'Heap's algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Heap%27s_algorithm",
    prerequisites=["permutation"],
))

# Spatial ext (tier 5)

register_atom(Atom(
    atom_type="algorithm", name="rotation_3d",
    content="3D rotation matrices: Rx(theta) rotates about x-axis, Ry about y, Rz about z. Each is a 3x3 orthogonal matrix with det=1. Composition: R = Rz*Ry*Rx (Euler angles). Alternative: quaternions avoid gimbal lock.",
    example="Rz(90 deg) * [1,0,0] = [0,1,0]. Point rotated 90 degrees about z-axis.",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Rotation matrix', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rotation_matrix",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm", name="voronoi_cell",
    content="A Voronoi diagram partitions space into cells, one per site, where each cell contains all points closer to its site than any other. Cell boundaries are perpendicular bisectors of segments connecting neighbouring sites.",
    example="Sites: (0,0), (4,0), (2,3). Voronoi cell of (0,0) bounded by bisectors of segments to (4,0) and (2,3).",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Voronoi diagram', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Voronoi_diagram",
    prerequisites=["midpoint"],
))

register_atom(Atom(
    atom_type="concept", name="delaunay_check",
    content="A Delaunay triangulation has the property that no point lies inside any triangle's circumcircle. Maximises the minimum angle. Dual of the Voronoi diagram. InCircle test checks if point d is inside the circumcircle of triangle abc.",
    example="Triangle (0,0),(1,0),(0,1). Circumcircle centre (0.5,0.5), radius sqrt(0.5). Point (0.4,0.4) is inside -> not Delaunay if part of another triangle.",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Delaunay triangulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Delaunay_triangulation",
    prerequisites=["circle_from_three_points"],
))

register_atom(Atom(
    atom_type="algorithm", name="convex_hull_2d",
    content="The convex hull is the smallest convex polygon containing all points. Graham scan: sort by polar angle from lowest point, process points maintaining left turns only. Complexity O(n log n). Jarvis march (gift wrapping) is O(nh).",
    example="Points: (0,0),(1,0),(0,1),(0.5,0.5),(1,1). Hull: (0,0),(1,0),(1,1),(0,1).",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Convex hull algorithms', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convex_hull_algorithms",
    prerequisites=["polygon_area"],
))

register_atom(Atom(
    atom_type="formula", name="affine_transform",
    content="An affine transformation maps points via y = A*x + b, where A is a linear transformation matrix and b is a translation vector. Preserves collinearity and ratios of distances. Composed as 3x3 homogeneous matrix.",
    example="Scale by 2 and translate by (1,3): A=[[2,0],[0,2]], b=[1,3]. Point (1,1) -> (2*1+1, 2*1+3) = (3,5).",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Affine transformation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Affine_transformation",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm", name="closest_pair",
    content="Find the closest pair of points in a set. Brute force: O(n^2). Divide and conquer: sort by x, split, recurse on halves, check strip of width 2*delta around dividing line. Complexity O(n log n).",
    example="Points (1,1),(3,2),(4,3),(6,1). Closest: (3,2)-(4,3), distance sqrt(2) = 1.414.",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Closest pair of points problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Closest_pair_of_points_problem",
    prerequisites=["distance_2d"],
))

# Spatial deep (tier 5)

register_atom(Atom(
    atom_type="algorithm", name="line_segment_intersection",
    content="Two line segments P1P2 and P3P4 intersect iff P1 and P2 are on opposite sides of line P3P4, AND P3 and P4 are on opposite sides of line P1P2. Computed using cross products: d1 = (P3P4) x (P3P1), d2 = (P3P4) x (P3P2). Intersect if d1*d2 < 0 and d3*d4 < 0.",
    example="Segments (0,0)-(2,2) and (0,2)-(2,0): d1 = 4, d2 = -4. d1*d2 < 0 -> intersect at (1,1).",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Line-line intersection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection",
    prerequisites=["cross_product"],
))

register_atom(Atom(
    atom_type="formula", name="point_in_triangle",
    content="Point P is inside triangle ABC if all barycentric coordinates (u,v,w) are non-negative and sum to 1. u = area(PBC)/area(ABC), v = area(APC)/area(ABC), w = 1-u-v. Equivalently, P is on the same side of all three edges.",
    example="A=(0,0), B=(4,0), C=(0,3), P=(1,1). area(ABC)=6, area(PBC)=3.5, u=3.5/6=0.583. v=2/6=0.333. w=0.083. All positive -> inside.",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Barycentric coordinate system', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Barycentric_coordinate_system",
    prerequisites=["polygon_area"],
))

register_atom(Atom(
    atom_type="formula", name="polygon_centroid",
    content="The centroid of a polygon with vertices (x_i, y_i): C_x = (1/(6A)) * sum((x_i+x_{i+1})*(x_i*y_{i+1}-x_{i+1}*y_i)), C_y similarly, where A is the signed area from the shoelace formula.",
    example="Triangle (0,0),(4,0),(0,3). A=6. C_x = (0+4+0)/3 = 1.333. C_y = (0+0+3)/3 = 1. Centroid (1.333, 1).",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Centroid', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Centroid#Of_a_polygon",
    prerequisites=["polygon_area"],
))

register_atom(Atom(
    atom_type="algorithm", name="minimum_bounding_circle",
    content="The minimum enclosing circle of a point set can be found in O(n) expected time (Welzl's algorithm). The circle is defined by at most 3 points on its boundary. Recursively: if a point lies outside the current circle, it must be on the boundary of the new circle.",
    example="Points (0,0),(1,0),(0,1). Circle centre (0.5,0.5), radius sqrt(0.5) ~ 0.707.",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Smallest-circle problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Smallest-circle_problem",
    prerequisites=["circle_from_three_points"],
))

register_atom(Atom(
    atom_type="formula", name="plane_line_intersection",
    content="A line r(t) = p + t*d intersects plane n.x = c at t = (c - n.p)/(n.d). If n.d = 0, line is parallel (no intersection unless n.p = c). The intersection point is r(t) = p + t*d.",
    example="Line: p=(1,0,0), d=(0,0,1). Plane: z=3 (n=(0,0,1), c=3). t = (3-0)/1 = 3. Point: (1,0,3).",
    tier=5, domain="geometry",
    source="Wikipedia contributors, 'Line-plane intersection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection",
    prerequisites=["dot_product"],
))
