"""Knowledge atoms for number theory deep and deep2 generators.

Covers Fermat's little theorem, Wilson's theorem, Euler criterion,
Carmichael numbers, discrete logarithm, Miller-Rabin, Legendre symbols,
Hensel lifting, Mobius inversion, and more. Each atom has a worked
example with known input and solution.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ── number_theory_deep ────────────────────────────────────────────

register_atom(Atom(
    atom_type="theorem",
    name="fermat_little",
    content=(
        "Fermat's little theorem states that if p is a prime number, "
        "then for any integer a not divisible by p, a^(p-1) is "
        "congruent to 1 modulo p. Equivalently, a^p is congruent to "
        "a modulo p for every integer a."
    ),
    example=(
        "a=3, p=7: 3^(7-1) = 3^6 = 729. "
        "729 mod 7 = 729 - 104*7 = 729 - 728 = 1. Verified."
    ),
    tier=5,
    domain="number_theory",
    source="Wikipedia contributors, 'Fermat's little theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fermat%27s_little_theorem",
    prerequisites=["modular", "exponentiation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="wilson_theorem",
    content=(
        "Wilson's theorem states that a natural number n > 1 is a "
        "prime number if and only if (n-1)! is congruent to -1 "
        "(mod n). That is, (n-1)! + 1 is divisible by n."
    ),
    example=(
        "n=7 (prime): (7-1)! = 6! = 720. "
        "720 mod 7 = 720 - 102*7 = 720 - 714 = 6 = -1 mod 7. Verified."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Wilson's theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Wilson%27s_theorem",
    prerequisites=["modular", "primality"],
))

register_atom(Atom(
    atom_type="theorem",
    name="chinese_remainder_ext",
    content=(
        "The Chinese Remainder Theorem (CRT) states that if the "
        "moduli n1, n2, ..., nk are pairwise coprime, then the "
        "system of simultaneous congruences x = a1 (mod n1), "
        "x = a2 (mod n2), ..., x = ak (mod nk) has a unique "
        "solution modulo N = n1*n2*...*nk."
    ),
    example=(
        "x = 2 (mod 3), x = 3 (mod 5), x = 2 (mod 7). "
        "N = 3*5*7 = 105. Solution: x = 23. "
        "Check: 23 mod 3 = 2, 23 mod 5 = 3, 23 mod 7 = 2."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Chinese remainder theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chinese_remainder_theorem",
    prerequisites=["modular", "gcd"],
))

register_atom(Atom(
    atom_type="theorem",
    name="euler_criterion",
    content=(
        "Euler's criterion states that for an odd prime p and an "
        "integer a not divisible by p, a is a quadratic residue "
        "modulo p if and only if a^((p-1)/2) is congruent to 1 "
        "(mod p). If a is a non-residue, then a^((p-1)/2) is "
        "congruent to -1 (mod p)."
    ),
    example=(
        "a=2, p=7: 2^((7-1)/2) = 2^3 = 8. "
        "8 mod 7 = 1. So 2 is a quadratic residue mod 7. "
        "Indeed, 3^2 = 9 = 2 (mod 7)."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Euler's criterion', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euler%27s_criterion",
    prerequisites=["modular", "exponentiation"],
))

register_atom(Atom(
    atom_type="definition",
    name="carmichael_number",
    content=(
        "A Carmichael number is a composite number n which satisfies "
        "the modular arithmetic congruence b^n = b (mod n) for all "
        "integers b. Equivalently, a Carmichael number is a composite "
        "n such that b^(n-1) = 1 (mod n) for all b coprime to n. "
        "By Korselt's criterion, n is Carmichael iff n is square-free "
        "and for each prime p dividing n, (p-1) divides (n-1)."
    ),
    example=(
        "n=561=3*11*17. Square-free: yes. "
        "p=3: (3-1)=2 divides (561-1)=560? 560/2=280, yes. "
        "p=11: (11-1)=10 divides 560? 560/10=56, yes. "
        "p=17: (17-1)=16 divides 560? 560/16=35, yes. "
        "561 is a Carmichael number."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Carmichael number', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Carmichael_number",
    prerequisites=["primality", "factorisation"],
))

register_atom(Atom(
    atom_type="definition",
    name="discrete_logarithm",
    content=(
        "The discrete logarithm of a number b to base g modulo p "
        "is the smallest non-negative integer x such that g^x = b "
        "(mod p). The discrete logarithm problem (DLP) is "
        "computationally hard for large primes, forming the basis "
        "of Diffie-Hellman key exchange and DSA."
    ),
    example=(
        "g=2, b=8, p=13: Find x such that 2^x = 8 (mod 13). "
        "2^1=2, 2^2=4, 2^3=8. So x=3."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Discrete logarithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Discrete_logarithm",
    prerequisites=["modular", "exponentiation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="miller_rabin",
    content=(
        "The Miller-Rabin primality test is a probabilistic test "
        "that determines whether a number is composite or probably "
        "prime. Write n-1 = 2^s * d with d odd. For a witness a, "
        "compute a^d mod n. If the result is 1 or n-1, n passes. "
        "Otherwise, square the result up to s-1 times; if any "
        "intermediate result is n-1, n passes. If none is, n is "
        "composite."
    ),
    example=(
        "n=221, a=174. n-1=220=2^2*55, so s=2, d=55. "
        "174^55 mod 221 = 47 (not 1 or 220). "
        "47^2 mod 221 = 2209 mod 221 = 220 = n-1. Passes. "
        "But 221=13*17 is composite (need more witnesses)."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Miller-Rabin primality test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test",
    prerequisites=["modular", "exponentiation", "primality"],
))

register_atom(Atom(
    atom_type="formula",
    name="sum_of_divisors_formula",
    content=(
        "The sum-of-divisors function sigma(n) gives the sum of all "
        "positive divisors of n. For a prime power p^a, "
        "sigma(p^a) = (p^(a+1) - 1) / (p - 1). Since sigma is "
        "multiplicative, for n = p1^a1 * p2^a2 * ..., "
        "sigma(n) = sigma(p1^a1) * sigma(p2^a2) * ..."
    ),
    example=(
        "n=12 = 2^2 * 3^1. "
        "sigma(2^2) = (2^3 - 1)/(2 - 1) = 7/1 = 7. "
        "sigma(3^1) = (3^2 - 1)/(3 - 1) = 8/2 = 4. "
        "sigma(12) = 7 * 4 = 28. "
        "Divisors: 1+2+3+4+6+12 = 28. Verified."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Divisor function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Divisor_function",
    prerequisites=["factorisation"],
))

register_atom(Atom(
    atom_type="definition",
    name="multiplicative_function",
    content=(
        "An arithmetic function f is multiplicative if f(1)=1 and "
        "f(mn) = f(m)*f(n) whenever gcd(m,n)=1. It is completely "
        "multiplicative if f(mn) = f(m)*f(n) for all m,n. "
        "Examples: Euler's totient phi(n), the Mobius function mu(n), "
        "and the divisor function sigma(n) are multiplicative."
    ),
    example=(
        "Euler's totient: phi(12) = phi(4)*phi(3) since gcd(4,3)=1. "
        "phi(4) = 4*(1-1/2) = 2. phi(3) = 3*(1-1/3) = 2. "
        "phi(12) = 2*2 = 4. "
        "Direct: {1,5,7,11} are coprime to 12, count=4. Verified."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Multiplicative function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Multiplicative_function",
    prerequisites=["totient", "gcd"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="perfect_power_test",
    content=(
        "A perfect power is a positive integer that can be expressed "
        "as a^b where a and b are positive integers with b >= 2. "
        "To test if n is a perfect power, check for each b from 2 "
        "to log2(n) whether n^(1/b) is an integer."
    ),
    example=(
        "n=125: b=2: sqrt(125)=11.18 (not integer). "
        "b=3: 125^(1/3) = 5.0 (integer). "
        "125 = 5^3 is a perfect power."
    ),
    tier=5,
    domain="number_theory",
    source="Wikipedia contributors, 'Perfect power', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Perfect_power",
    prerequisites=["exponentiation"],
))


# ── number_theory_deep2 ──────────────────────────────────────────

register_atom(Atom(
    atom_type="theorem",
    name="sum_of_four_squares",
    content=(
        "Lagrange's four-square theorem states that every natural "
        "number can be represented as the sum of four integer "
        "squares: n = a^2 + b^2 + c^2 + d^2. This was proved by "
        "Lagrange in 1770."
    ),
    example=(
        "n=7: 7 = 1^2 + 1^2 + 1^2 + 2^2 = 1 + 1 + 1 + 4 = 7. "
        "n=15: 15 = 1^2 + 1^2 + 2^2 + 3^2 = 1 + 1 + 4 + 9 = 15."
    ),
    tier=5,
    domain="number_theory",
    source="Wikipedia contributors, 'Lagrange's four-square theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="legendre_symbol_compute",
    content=(
        "The Legendre symbol (a/p) for an odd prime p and integer a "
        "is defined as: (a/p) = 0 if p divides a, 1 if a is a "
        "quadratic residue mod p, -1 if a is a quadratic non-residue "
        "mod p. It can be computed via Euler's criterion: "
        "(a/p) = a^((p-1)/2) mod p."
    ),
    example=(
        "a=3, p=11: 3^((11-1)/2) = 3^5 = 243. "
        "243 mod 11 = 243 - 22*11 = 243 - 242 = 1. "
        "So (3/11) = 1, meaning 3 is a quadratic residue mod 11. "
        "Indeed, 5^2 = 25 = 3 (mod 11)."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Legendre symbol', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Legendre_symbol",
    prerequisites=["euler_criterion"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="hensel_lift_ext",
    content=(
        "Hensel's lemma (or Hensel lifting) allows lifting a "
        "solution of a polynomial equation modulo a prime p to "
        "a solution modulo higher powers of p. If f(a) = 0 (mod p) "
        "and f'(a) != 0 (mod p), then there exists a unique lift "
        "a' such that f(a') = 0 (mod p^2), given by "
        "a' = a - f(a) * (f'(a))^(-1) (mod p^2)."
    ),
    example=(
        "f(x) = x^2 - 2, p=7, a=3 (since 3^2=9=2 mod 7). "
        "f(3) = 9-2 = 7. f'(x)=2x, f'(3)=6. "
        "6^(-1) mod 49: 6*41=246=5*49+1, so 6^(-1)=41 mod 49. "
        "a' = 3 - 7*41 = 3 - 287 = 3 - 5*49 - 42 = 3+7*(-41 mod 7) "
        "= 3 - 7*6 mod 49 = 3 + 7 = 10 mod 49. "
        "Check: 10^2 = 100 = 2*49 + 2, so 100 mod 49 = 2. Verified."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Hensel's lemma', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hensel%27s_lemma",
    prerequisites=["modular", "mod_inv"],
))

register_atom(Atom(
    atom_type="definition",
    name="dirichlet_character",
    content=(
        "A Dirichlet character modulo k is a completely "
        "multiplicative arithmetic function chi: Z -> C such that "
        "chi(n) = 0 if gcd(n,k) > 1, chi(n+k) = chi(n) for all n, "
        "and chi(1) = 1. The principal character chi_0 satisfies "
        "chi_0(n) = 1 if gcd(n,k) = 1 and 0 otherwise."
    ),
    example=(
        "k=4, principal character chi_0: "
        "chi_0(1)=1, chi_0(2)=0, chi_0(3)=1, chi_0(4)=0. "
        "Non-principal character chi_1: "
        "chi_1(1)=1, chi_1(2)=0, chi_1(3)=-1, chi_1(4)=0."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Dirichlet character', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dirichlet_character",
    prerequisites=["multiplicative_function", "totient"],
))

register_atom(Atom(
    atom_type="formula",
    name="mobius_inversion",
    content=(
        "The Mobius inversion formula states that if "
        "g(n) = sum_{d|n} f(d), then f(n) = sum_{d|n} mu(n/d)*g(d), "
        "where mu is the Mobius function: mu(n) = 1 if n=1, "
        "mu(n) = (-1)^k if n is a product of k distinct primes, "
        "mu(n) = 0 if n has a squared prime factor."
    ),
    example=(
        "g(n) = sum_{d|n} phi(d) = n (known identity). "
        "Invert: phi(n) = sum_{d|n} mu(n/d)*d. "
        "n=6: divisors {1,2,3,6}. "
        "mu(6)*1 + mu(3)*2 + mu(2)*3 + mu(1)*6 "
        "= 1*1 + (-1)*2 + (-1)*3 + 1*6 = 1-2-3+6 = 2 = phi(6)."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Mobius inversion formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/M%C3%B6bius_inversion_formula",
    prerequisites=["multiplicative_function", "totient"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="continued_fraction_convergent",
    content=(
        "The continued fraction expansion of a real number x is "
        "[a0; a1, a2, ...] where a0 = floor(x) and subsequent "
        "terms come from the reciprocal of the fractional part. "
        "The k-th convergent p_k/q_k is computed via the recurrence: "
        "p_k = a_k*p_{k-1} + p_{k-2}, q_k = a_k*q_{k-1} + q_{k-2}, "
        "with p_{-1}=1, p_{-2}=0, q_{-1}=0, q_{-2}=1."
    ),
    example=(
        "sqrt(2) = [1; 2, 2, 2, ...]. "
        "Convergents: 1/1, 3/2, 7/5, 17/12, 41/29. "
        "p0=1,q0=1. p1=2*1+1=3,q1=2*1+0=2. "
        "p2=2*3+1=7,q2=2*2+1=5. 7/5=1.4 (sqrt(2)=1.4142...)."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Continued fraction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Continued_fraction",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="fibonacci_mod",
    content=(
        "The Fibonacci sequence modulo m is periodic (Pisano period). "
        "F(n) mod m can be computed efficiently using matrix "
        "exponentiation: [[F(n+1), F(n)], [F(n), F(n-1)]] = "
        "[[1,1],[1,0]]^n. The Pisano period pi(m) is the period "
        "of F(n) mod m."
    ),
    example=(
        "F(10) mod 7: F(10)=55. 55 mod 7 = 55-7*7 = 55-49 = 6. "
        "Pisano period pi(7): F mod 7 sequence is "
        "0,1,1,2,3,5,1,6,0,6,6,5,4,2,6,1,0,1,... period=16."
    ),
    tier=4,
    domain="number_theory",
    source="Wikipedia contributors, 'Pisano period', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pisano_period",
    prerequisites=["fibonacci", "modular"],
))

register_atom(Atom(
    atom_type="rule",
    name="digit_sum_divisibility",
    content=(
        "Divisibility rules based on digit sums: a number is "
        "divisible by 3 if its digit sum is divisible by 3; "
        "divisible by 9 if its digit sum is divisible by 9. "
        "This works because 10 = 1 (mod 3) and 10 = 1 (mod 9), "
        "so any number equals its digit sum modulo 3 or 9."
    ),
    example=(
        "n=1728: digit sum = 1+7+2+8 = 18. "
        "18 is divisible by 3: yes (18/3=6). So 1728 is divisible by 3. "
        "18 is divisible by 9: yes (18/9=2). So 1728 is divisible by 9. "
        "Check: 1728/9 = 192."
    ),
    tier=3,
    domain="number_theory",
    source="Wikipedia contributors, 'Divisibility rule', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Divisibility_rule",
    prerequisites=["digit_root", "modular"],
))

register_atom(Atom(
    atom_type="formula",
    name="modular_equation",
    content=(
        "A modular equation ax = b (mod m) has a solution if and "
        "only if gcd(a, m) divides b. When d = gcd(a, m) divides b, "
        "there are exactly d solutions modulo m, given by "
        "x = (b/d) * (a/d)^(-1) (mod m/d) plus multiples of m/d."
    ),
    example=(
        "6x = 4 (mod 10). gcd(6,10)=2. 2 divides 4, so solutions exist. "
        "Reduce: 3x = 2 (mod 5). 3^(-1) mod 5 = 2 (since 3*2=6=1 mod 5). "
        "x = 2*2 = 4 (mod 5). Solutions mod 10: x=4 and x=9."
    ),
    tier=5,
    domain="number_theory",
    source="Wikipedia contributors, 'Modular arithmetic', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Modular_arithmetic#Modular_equation",
    prerequisites=["modular", "gcd", "mod_inv"],
))

register_atom(Atom(
    atom_type="formula",
    name="prime_counting",
    content=(
        "The prime-counting function pi(x) gives the number of "
        "primes less than or equal to x. The prime number theorem "
        "states that pi(x) ~ x/ln(x) as x -> infinity. Better "
        "approximations include pi(x) ~ Li(x) = integral from 2 to "
        "x of 1/ln(t) dt."
    ),
    example=(
        "pi(10) = 4 (primes: 2, 3, 5, 7). "
        "pi(100) = 25. Approximation: 100/ln(100) = 100/4.605 = 21.7 "
        "(within 13% of actual 25)."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia contributors, 'Prime-counting function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Prime-counting_function",
    prerequisites=["primality"],
))
