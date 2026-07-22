"""Knowledge atoms for cryptography and functional analysis.

Covers RSA, Diffie-Hellman, ElGamal, digital signatures, elliptic
curves, hash-based constructions, and core functional analysis theorems
including Banach spaces, Hilbert spaces, and operator theory.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Cryptography (tier 4-6)
# =========================================================================

register_atom(Atom(
    atom_type="algorithm",
    name="rsa_keygen",
    content=(
        "RSA key generation selects two large primes p and q, computes "
        "n = p*q and phi(n) = (p-1)*(q-1). A public exponent e is chosen "
        "coprime to phi(n), typically e = 65537. The private exponent d "
        "is computed as the modular inverse of e modulo phi(n): "
        "d = e^{-1} mod phi(n). The public key is (n, e) and the private "
        "key is (n, d)."
    ),
    example=(
        "p=61, q=53: n = 61*53 = 3233, phi = 60*52 = 3120, e = 17, "
        "d = 17^{-1} mod 3120 = 2753. Public key: (3233, 17), "
        "private key: (3233, 2753)."
    ),
    tier=6,
    domain="cryptography",
    source="Wikipedia contributors, 'RSA (cryptosystem)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/RSA_(cryptosystem)",
    prerequisites=["mod_pow", "mod_inv", "primality"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="rsa_encrypt",
    content=(
        "RSA encryption computes the ciphertext c from a plaintext "
        "message m using the public key (n, e): c = m^e mod n. "
        "The message m must satisfy 0 <= m < n."
    ),
    example=(
        "Public key (n=3233, e=17), plaintext m=65: "
        "c = 65^17 mod 3233 = 2790."
    ),
    tier=6,
    domain="cryptography",
    source="Wikipedia contributors, 'RSA (cryptosystem)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/RSA_(cryptosystem)",
    prerequisites=["mod_pow"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="rsa_decrypt",
    content=(
        "RSA decryption recovers the plaintext m from ciphertext c "
        "using the private key (n, d): m = c^d mod n. By Euler's "
        "theorem, m^{ed} = m mod n, so decryption reverses encryption."
    ),
    example=(
        "Private key (n=3233, d=2753), ciphertext c=2790: "
        "m = 2790^2753 mod 3233 = 65."
    ),
    tier=6,
    domain="cryptography",
    source="Wikipedia contributors, 'RSA (cryptosystem)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/RSA_(cryptosystem)",
    prerequisites=["mod_pow"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="diffie_hellman",
    content=(
        "The Diffie-Hellman key exchange allows two parties to establish "
        "a shared secret over an insecure channel. Both agree on a prime "
        "p and generator g. Alice picks secret a, sends A = g^a mod p. "
        "Bob picks secret b, sends B = g^b mod p. Both compute the "
        "shared secret: s = B^a mod p = A^b mod p = g^{ab} mod p."
    ),
    example=(
        "p=23, g=5: Alice a=6, A = 5^6 mod 23 = 8. Bob b=15, "
        "B = 5^15 mod 23 = 19. Shared: s = 19^6 mod 23 = 2 = 8^15 mod 23."
    ),
    tier=6,
    domain="cryptography",
    source=(
        "Wikipedia contributors, 'Diffie-Hellman key exchange', Wikipedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange",
    prerequisites=["mod_pow"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="digital_signature",
    content=(
        "A digital signature scheme consists of key generation, signing, "
        "and verification. In RSA signing, the signer computes s = m^d "
        "mod n using the private key. The verifier checks m = s^e mod n "
        "using the public key. If the recovered message matches the "
        "original, the signature is valid."
    ),
    example=(
        "RSA sign: private key (n=3233, d=2753), message hash h=100. "
        "Signature s = 100^2753 mod 3233 = 2627. "
        "Verify: 2627^17 mod 3233 = 100. Valid."
    ),
    tier=6,
    domain="cryptography",
    source=(
        "Wikipedia contributors, 'Digital signature', Wikipedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Digital_signature",
    prerequisites=["rsa_keygen"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="elliptic_curve_add",
    content=(
        "Elliptic curve point addition on y^2 = x^3 + ax + b over a "
        "finite field. Given points P=(x1,y1) and Q=(x2,y2), the sum "
        "R = P + Q has coordinates: lambda = (y2-y1)/(x2-x1), "
        "x3 = lambda^2 - x1 - x2, y3 = lambda*(x1-x3) - y1. "
        "For point doubling (P=Q): lambda = (3*x1^2 + a)/(2*y1)."
    ),
    example=(
        "Curve y^2 = x^3 + 2x + 3 over F_97. P=(3,6), Q=(80,10). "
        "lambda = (10-6)/(80-3) = 4/77 = 4*77^{-1} mod 97. "
        "77^{-1} mod 97 = 54. lambda = 4*54 mod 97 = 216 mod 97 = 22. "
        "x3 = 22^2 - 3 - 80 = 484 - 83 = 401 mod 97 = 13. "
        "y3 = 22*(3-13) - 6 = -220 - 6 = -226 mod 97 = 65. R=(13,65)."
    ),
    tier=6,
    domain="cryptography",
    source=(
        "Wikipedia contributors, 'Elliptic curve point multiplication', "
        "Wikipedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication",
    prerequisites=["mod_inv"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="otp_encrypt",
    content=(
        "The one-time pad (OTP) is an encryption technique where each "
        "plaintext character is combined with a character from a random "
        "key of equal length using modular addition. For binary: "
        "c_i = p_i XOR k_i. OTP is information-theoretically secure "
        "when the key is truly random, used only once, and kept secret."
    ),
    example=(
        "Plaintext 'HI' = [7, 8], key = [12, 3], mod 26: "
        "c = [(7+12) mod 26, (8+3) mod 26] = [19, 11] = 'TL'."
    ),
    tier=4,
    domain="cryptography",
    source="Wikipedia contributors, 'One-time pad', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/One-time_pad",
    prerequisites=["modular"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="feistel_round",
    content=(
        "A Feistel cipher splits the plaintext block into two halves "
        "(L, R) and applies rounds of the form: L_{i+1} = R_i, "
        "R_{i+1} = L_i XOR F(R_i, K_i), where F is the round function "
        "and K_i is the subkey. Decryption uses the same structure with "
        "subkeys in reverse order."
    ),
    example=(
        "L0=0101, R0=1010, F(R,K) = R XOR K, K1=1100. "
        "L1 = R0 = 1010. R1 = L0 XOR F(R0, K1) = 0101 XOR (1010 XOR 1100) "
        "= 0101 XOR 0110 = 0011. After 1 round: (1010, 0011)."
    ),
    tier=5,
    domain="cryptography",
    source="Wikipedia contributors, 'Feistel cipher', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Feistel_cipher",
    prerequisites=["binary_arithmetic"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="hash_collision",
    content=(
        "A hash collision occurs when two distinct inputs produce the "
        "same hash output: H(m1) = H(m2) with m1 != m2. By the birthday "
        "paradox, for a hash with n-bit output, a collision is expected "
        "after approximately 2^{n/2} random inputs. Finding collisions "
        "is central to cryptanalysis of hash functions."
    ),
    example=(
        "Hash with 4-bit output (16 possible values). Birthday bound: "
        "2^{4/2} = 4 trials expected. After hashing 5 random inputs, "
        "probability of collision > 50%."
    ),
    tier=5,
    domain="cryptography",
    source="Wikipedia contributors, 'Collision (hash function)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hash_collision",
    prerequisites=["hash_function"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="elgamal_encrypt",
    content=(
        "ElGamal encryption uses a cyclic group of prime order p with "
        "generator g. Public key: h = g^x mod p (x is private). "
        "To encrypt message m: pick random k, compute c1 = g^k mod p, "
        "c2 = m * h^k mod p. Ciphertext is (c1, c2). "
        "Decrypt: m = c2 * (c1^x)^{-1} mod p."
    ),
    example=(
        "p=23, g=5, x=6, h = 5^6 mod 23 = 8. "
        "Encrypt m=7, k=3: c1 = 5^3 mod 23 = 10, "
        "c2 = 7 * 8^3 mod 23 = 7 * 512 mod 23 = 7 * 6 mod 23 = 42 mod 23 = 19. "
        "Ciphertext: (10, 19)."
    ),
    tier=6,
    domain="cryptography",
    source="Wikipedia contributors, 'ElGamal encryption', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/ElGamal_encryption",
    prerequisites=["diffie_hellman", "mod_inv"],
))


# =========================================================================
# Functional Analysis (tier 5-7)
# =========================================================================

register_atom(Atom(
    atom_type="definition",
    name="norm_compute",
    content=(
        "A norm on a vector space V is a function ||.||: V -> R satisfying "
        "(1) ||x|| >= 0 with equality iff x = 0, (2) ||alpha*x|| = "
        "|alpha|*||x||, (3) ||x + y|| <= ||x|| + ||y|| (triangle "
        "inequality). Common norms: L1 = sum|x_i|, L2 = sqrt(sum x_i^2), "
        "Linf = max|x_i|."
    ),
    example=(
        "x = (3, -4): L1 = |3| + |-4| = 7, "
        "L2 = sqrt(9 + 16) = sqrt(25) = 5, "
        "Linf = max(3, 4) = 4."
    ),
    tier=5,
    domain="functional_analysis",
    source="Wikipedia contributors, 'Norm (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Norm_(mathematics)",
    prerequisites=["absolute_value"],
))

register_atom(Atom(
    atom_type="definition",
    name="banach_space_check",
    content=(
        "A Banach space is a complete normed vector space, meaning every "
        "Cauchy sequence in the space converges to a limit within the "
        "space. R^n with any p-norm is a Banach space. The space C[a,b] "
        "of continuous functions with the sup norm is a Banach space. "
        "The space of polynomials with the sup norm on [0,1] is NOT "
        "Banach (not closed under limits)."
    ),
    example=(
        "Is (R^3, ||.||_2) a Banach space? R^3 is finite-dimensional, "
        "so all norms are equivalent and the space is complete. Yes, "
        "it is a Banach space."
    ),
    tier=6,
    domain="functional_analysis",
    source="Wikipedia contributors, 'Banach space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Banach_space",
    prerequisites=["norm_compute", "cauchy_sequence"],
))

register_atom(Atom(
    atom_type="definition",
    name="inner_product_verify",
    content=(
        "An inner product on a vector space V over F (R or C) is a map "
        "<.,.>: V x V -> F satisfying (1) <x,x> >= 0 with equality iff "
        "x = 0, (2) <x,y> = conjugate(<y,x>), (3) linearity in the "
        "first argument: <ax+by, z> = a<x,z> + b<y,z>. The standard "
        "inner product on R^n is <x,y> = sum x_i*y_i."
    ),
    example=(
        "x = (1, 2, 3), y = (4, 5, 6): <x,y> = 1*4 + 2*5 + 3*6 = "
        "4 + 10 + 18 = 32. ||x|| = sqrt(<x,x>) = sqrt(1+4+9) = sqrt(14)."
    ),
    tier=5,
    domain="functional_analysis",
    source="Wikipedia contributors, 'Inner product space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inner_product_space",
    prerequisites=["dot_product"],
))

register_atom(Atom(
    atom_type="formula",
    name="orthogonal_projection",
    content=(
        "The orthogonal projection of vector v onto subspace W spanned "
        "by an orthonormal basis {u_1, ..., u_k} is: "
        "proj_W(v) = sum_i <v, u_i> u_i. For projection onto a single "
        "vector u: proj_u(v) = (<v,u> / <u,u>) * u."
    ),
    example=(
        "v = (3, 4), u = (1, 0): proj_u(v) = (<(3,4),(1,0)> / "
        "<(1,0),(1,0)>) * (1,0) = (3/1) * (1,0) = (3, 0)."
    ),
    tier=6,
    domain="functional_analysis",
    source=(
        "Wikipedia contributors, 'Projection (linear algebra)', Wikipedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Projection_(linear_algebra)",
    prerequisites=["inner_product_verify", "gram_schmidt"],
))

register_atom(Atom(
    atom_type="definition",
    name="adjoint_operator",
    content=(
        "The adjoint of a bounded linear operator T on a Hilbert space H "
        "is the unique operator T* satisfying <Tx, y> = <x, T*y> for all "
        "x, y in H. For matrices, the adjoint is the conjugate transpose: "
        "A* = conjugate(A^T). An operator is self-adjoint if T = T*."
    ),
    example=(
        "A = [[1, 2+i], [3, 4]]: A* = conjugate(A^T) = "
        "[[1, 3], [2-i, 4]]. "
        "Check: <Ax, y> = <x, A*y> for all x, y."
    ),
    tier=6,
    domain="functional_analysis",
    source="Wikipedia contributors, 'Hermitian adjoint', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hermitian_adjoint",
    prerequisites=["inner_product_verify", "matrix_transpose"],
))

register_atom(Atom(
    atom_type="theorem",
    name="spectral_decomposition",
    content=(
        "The spectral theorem states that every self-adjoint (Hermitian) "
        "operator on a finite-dimensional inner product space has an "
        "orthonormal basis of eigenvectors. For a matrix A = A*, the "
        "spectral decomposition is A = U * diag(lambda_1, ..., lambda_n) "
        "* U*, where U is unitary and lambda_i are real eigenvalues."
    ),
    example=(
        "A = [[2, 1], [1, 2]] (symmetric, so A=A*). "
        "Eigenvalues: det(A - lambda*I) = (2-lambda)^2 - 1 = 0, "
        "lambda = 3 or 1. "
        "A = U*diag(3,1)*U^T with U = [[1/sqrt(2), 1/sqrt(2)], "
        "[1/sqrt(2), -1/sqrt(2)]]."
    ),
    tier=6,
    domain="functional_analysis",
    source="Wikipedia contributors, 'Spectral theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Spectral_theorem",
    prerequisites=["eigenvalue", "adjoint_operator"],
))

register_atom(Atom(
    atom_type="definition",
    name="compact_operator",
    content=(
        "A bounded linear operator T: X -> Y between Banach spaces is "
        "compact if it maps bounded sets to relatively compact sets "
        "(sets whose closure is compact). Equivalently, every bounded "
        "sequence {x_n} has a subsequence such that {Tx_{n_k}} "
        "converges. Finite-rank operators are always compact. "
        "On infinite-dimensional spaces, the identity is NOT compact."
    ),
    example=(
        "T: l^2 -> l^2 defined by T(x_1, x_2, ...) = (x_1, x_2/2, "
        "x_3/3, ...). T is compact because the partial sums T_n (keeping "
        "first n terms, zeroing rest) are finite-rank, and ||T - T_n|| "
        "= 1/(n+1) -> 0."
    ),
    tier=7,
    domain="functional_analysis",
    source="Wikipedia contributors, 'Compact operator', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Compact_operator",
    prerequisites=["banach_space_check", "norm_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="dual_space",
    content=(
        "The dual space V* of a normed vector space V is the space of "
        "all bounded linear functionals f: V -> F, with norm "
        "||f|| = sup{|f(x)| : ||x|| <= 1}. For R^n, the dual is "
        "isomorphic to R^n itself. For l^p, the dual is l^q where "
        "1/p + 1/q = 1."
    ),
    example=(
        "V = R^3, f(x) = 2*x_1 + 3*x_2 - x_3. "
        "||f|| = sup{|2x_1+3x_2-x_3| : ||(x_1,x_2,x_3)||_2 <= 1} = "
        "sqrt(4+9+1) = sqrt(14) (by Cauchy-Schwarz)."
    ),
    tier=6,
    domain="functional_analysis",
    source="Wikipedia contributors, 'Dual space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dual_space",
    prerequisites=["norm_compute", "inner_product_verify"],
))

register_atom(Atom(
    atom_type="theorem",
    name="hahn_banach_apply",
    content=(
        "The Hahn-Banach theorem states that a bounded linear functional "
        "defined on a subspace of a normed space can be extended to the "
        "entire space without increasing its norm. Formally: if M is a "
        "subspace of X and f: M -> R is bounded with ||f||_M = c, then "
        "there exists F: X -> R extending f with ||F||_X = c."
    ),
    example=(
        "X = R^3, M = span{(1,0,0), (0,1,0)}, f(a,b,0) = 2a + 3b. "
        "||f||_M = sqrt(4+9) = sqrt(13). "
        "Extension: F(a,b,c) = 2a + 3b + 0*c. ||F||_X = sqrt(13) = ||f||_M."
    ),
    tier=7,
    domain="functional_analysis",
    source="Wikipedia contributors, 'Hahn-Banach theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hahn%E2%80%93Banach_theorem",
    prerequisites=["dual_space", "norm_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="riesz_representation",
    content=(
        "The Riesz representation theorem states that for every bounded "
        "linear functional f on a Hilbert space H, there exists a unique "
        "element y in H such that f(x) = <x, y> for all x in H, and "
        "||f|| = ||y||. This establishes an isometric isomorphism between "
        "H and its dual H*."
    ),
    example=(
        "H = R^3 with standard inner product. f(x) = 2x_1 + 3x_2 - x_3. "
        "By Riesz, y = (2, 3, -1) and f(x) = <x, y> = 2x_1 + 3x_2 - x_3. "
        "||f|| = ||y|| = sqrt(4+9+1) = sqrt(14)."
    ),
    tier=7,
    domain="functional_analysis",
    source=(
        "Wikipedia contributors, 'Riesz representation theorem', Wikipedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Riesz_representation_theorem",
    prerequisites=["inner_product_verify", "dual_space"],
))
