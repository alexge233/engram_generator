"""Knowledge atoms for extended cryptography generators."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

register_atom(Atom(
    atom_type="algorithm",
    name="dsa_sign",
    content=(
        "The Digital Signature Algorithm (DSA) produces a digital signature "
        "(r, s) for a message hash h using a private key x and domain "
        "parameters (p, q, g). Choose random k in [1, q-1], compute "
        "r = (g^k mod p) mod q, s = k^{-1}(h + x*r) mod q. The signature "
        "is verified by checking that r == (g^{s^{-1}*h} * y^{s^{-1}*r} mod p) mod q "
        "where y = g^x mod p is the public key."
    ),
    example=(
        "With p=23, q=11, g=4, x=7, h=5, k=3: "
        "r = (4^3 mod 23) mod 11 = 64 mod 23 mod 11 = 18 mod 11 = 7. "
        "k^{-1} mod 11 = 4. s = 4*(5 + 7*7) mod 11 = 4*54 mod 11 = 216 mod 11 = 7."
    ),
    tier=6,
    domain="crypto_ext",
    source="Wikipedia contributors, 'Digital Signature Algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Digital_Signature_Algorithm",
    prerequisites=["modpow", "modinv"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="shamir_secret_share",
    content=(
        "Shamir's Secret Sharing splits a secret s into n shares such that "
        "any k shares can reconstruct s but k-1 shares reveal nothing. "
        "Choose a random polynomial f(x) of degree k-1 with f(0) = s over "
        "a finite field GF(p). Each share is (i, f(i)) for i = 1..n. "
        "Reconstruction uses Lagrange interpolation to recover f(0) = s."
    ),
    example=(
        "Secret s=42, k=2, n=3, p=97. Choose f(x) = 42 + 17x mod 97. "
        "Shares: (1, 59), (2, 76), (3, 93). Any 2 shares reconstruct: "
        "L_1(0) = -2/(-1) = 2, L_2(0) = -1/(1) = -1. "
        "s = 59*2 + 76*(-1) = 118 - 76 = 42."
    ),
    tier=5,
    domain="crypto_ext",
    source="Wikipedia contributors, 'Shamir's secret sharing', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="definition",
    name="commitment_scheme",
    content=(
        "A commitment scheme allows a party to commit to a value while "
        "keeping it hidden, then reveal it later. A Pedersen commitment "
        "is C = g^m * h^r mod p where m is the message, r is a random "
        "blinding factor, and g, h are generators. It is computationally "
        "hiding (can't determine m from C) and perfectly binding "
        "(can't open to a different value)."
    ),
    example=(
        "With g=4, h=9, p=23, m=5, r=3: "
        "C = 4^5 * 9^3 mod 23 = 1024 * 729 mod 23 = 12 * 16 mod 23 = 192 mod 23 = 8."
    ),
    tier=5,
    domain="crypto_ext",
    source="Wikipedia contributors, 'Commitment scheme', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Commitment_scheme",
    prerequisites=["modpow"],
))

register_atom(Atom(
    atom_type="definition",
    name="zero_knowledge_basic",
    content=(
        "A zero-knowledge proof allows a prover to convince a verifier "
        "that a statement is true without revealing any information "
        "beyond the truth of the statement. The protocol satisfies: "
        "completeness (honest prover convinces verifier), soundness "
        "(dishonest prover fails), and zero-knowledge (verifier learns "
        "nothing). Schnorr's protocol proves knowledge of discrete log."
    ),
    example=(
        "Schnorr ZK for y=g^x mod p: Prover picks random r, sends "
        "t=g^r mod p. Verifier sends challenge c. Prover responds "
        "s=r+c*x mod q. Verifier checks g^s == t*y^c mod p."
    ),
    tier=6,
    domain="crypto_ext",
    source="Wikipedia contributors, 'Zero-knowledge proof', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Zero-knowledge_proof",
    prerequisites=["modpow"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="merkle_tree",
    content=(
        "A Merkle tree is a binary tree of hash values where each leaf "
        "is the hash of a data block and each internal node is the hash "
        "of its two children: H(left || right). The root hash summarises "
        "all data. Membership proofs require O(log n) hashes. Any change "
        "to a leaf propagates to the root."
    ),
    example=(
        "Data blocks [A, B, C, D]. Leaves: h(A), h(B), h(C), h(D). "
        "Internal: h(h(A)||h(B)), h(h(C)||h(D)). Root: h(h(h(A)||h(B))||h(h(C)||h(D))). "
        "Proof for B: provide h(A) and h(h(C)||h(D)), verify 2 hashes."
    ),
    tier=5,
    domain="crypto_ext",
    source="Wikipedia contributors, 'Merkle tree', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Merkle_tree",
    prerequisites=["hash_chain"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="stream_cipher",
    content=(
        "A stream cipher encrypts plaintext one bit or byte at a time by "
        "XORing it with a pseudorandom keystream generated from a secret "
        "key and IV. Ciphertext c_i = p_i XOR k_i. Decryption is the "
        "same operation: p_i = c_i XOR k_i. Security depends on the "
        "keystream being unpredictable. Examples: RC4, ChaCha20."
    ),
    example=(
        "Key stream: [0x3A, 0x7F]. Plaintext: [0x48, 0x69] ('Hi'). "
        "Ciphertext: [0x48 XOR 0x3A, 0x69 XOR 0x7F] = [0x72, 0x16]. "
        "Decrypt: [0x72 XOR 0x3A, 0x16 XOR 0x7F] = [0x48, 0x69] = 'Hi'."
    ),
    tier=5,
    domain="crypto_ext",
    source="Wikipedia contributors, 'Stream cipher', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stream_cipher",
    prerequisites=["otp_encrypt"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="block_cipher_modes",
    content=(
        "Block cipher modes of operation define how to apply a block cipher "
        "to data longer than one block. ECB encrypts each block independently "
        "(insecure for patterns). CBC XORs each plaintext block with the "
        "previous ciphertext block before encryption: C_i = E_K(P_i XOR C_{i-1}). "
        "CTR mode turns the block cipher into a stream cipher by encrypting "
        "counter values."
    ),
    example=(
        "CBC mode with block size 8, IV=0x00: P1=0xAB, P2=0xCD. "
        "C1 = E_K(P1 XOR IV) = E_K(0xAB). "
        "C2 = E_K(P2 XOR C1) = E_K(0xCD XOR C1)."
    ),
    tier=5,
    domain="crypto_ext",
    source="Wikipedia contributors, 'Block cipher mode of operation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation",
    prerequisites=["feistel_round"],
))
