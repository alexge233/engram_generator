"""Knowledge atoms for open problems in mathematics.

Covers conjectures and computational structures related to unsolved
problems: Riemann Hypothesis, Goldbach, Twin Primes, Erdos-Straus,
Legendre, Waring, ABC, Beal, Brocard, and P vs NP.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


register_atom(Atom(
    atom_type="formula",
    name="zeta_partial_sum",
    content=(
        "The Riemann zeta function is defined for complex s with Re(s) > 1 "
        "by the series zeta(s) = sum_{n=1}^{infinity} 1/n^s. A partial sum "
        "approximation uses the first N terms: zeta_N(s) = sum_{n=1}^{N} "
        "1/n^s. The Riemann Hypothesis conjectures that all non-trivial "
        "zeros of zeta(s) have real part equal to 1/2."
    ),
    example=(
        "zeta_3(2) = 1/1^2 + 1/2^2 + 1/3^2 = 1 + 0.25 + 0.1111 = 1.3611. "
        "Exact: zeta(2) = pi^2/6 = 1.6449."
    ),
    tier=5,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Riemann zeta function', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Riemann_zeta_function",
    prerequisites=["exponentiation", "summation"],
))

register_atom(Atom(
    atom_type="formula",
    name="euler_product",
    content=(
        "The Euler product formula expresses the Riemann zeta function as "
        "an infinite product over all primes p: zeta(s) = prod_{p prime} "
        "1/(1 - p^{-s}) for Re(s) > 1. This identity links the zeta "
        "function to the distribution of prime numbers and is the basis "
        "for analytic number theory."
    ),
    example=(
        "First 3 primes: prod = 1/(1-2^{-2}) * 1/(1-3^{-2}) * 1/(1-5^{-2}) "
        "= 1/0.75 * 1/0.8889 * 1/0.96 = 1.3333 * 1.125 * 1.0417 = 1.5625. "
        "Converges toward zeta(2) = pi^2/6 = 1.6449."
    ),
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Euler product', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Euler_product",
    prerequisites=["zeta_partial_sum", "primality"],
))

register_atom(Atom(
    atom_type="conjecture",
    name="goldbach_partition",
    content=(
        "Goldbach's conjecture states that every even integer greater than "
        "2 can be expressed as the sum of two prime numbers. For example, "
        "4 = 2+2, 6 = 3+3, 8 = 3+5. The conjecture has been verified "
        "computationally for all even numbers up to 4 x 10^18 but remains "
        "unproven. The task is to find a Goldbach partition for a given "
        "even number."
    ),
    example="28 = 5 + 23 (both 5 and 23 are prime).",
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Goldbach's conjecture', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Goldbach%27s_conjecture",
    prerequisites=["primality", "addition"],
))

register_atom(Atom(
    atom_type="conjecture",
    name="twin_prime_search",
    content=(
        "Twin primes are pairs of primes that differ by 2. Examples: "
        "(3,5), (5,7), (11,13), (17,19), (29,31). The Twin Prime "
        "Conjecture asserts that there are infinitely many twin prime "
        "pairs. In 2013, Yitang Zhang proved there are infinitely many "
        "pairs of primes differing by at most 70 million; this bound "
        "has since been reduced to 246."
    ),
    example=(
        "Search [10,20]: 11 is prime, 13 is prime, 13-11=2 -> (11,13) "
        "is a twin prime pair."
    ),
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Twin prime', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Twin_prime",
    prerequisites=["primality"],
))

register_atom(Atom(
    atom_type="definition",
    name="perfect_number_check",
    content=(
        "A perfect number is a positive integer that equals the sum of "
        "its proper divisors (all divisors except itself). The first "
        "four perfect numbers are 6, 28, 496, and 8128. Euler proved "
        "that every even perfect number has the form 2^{p-1}(2^p - 1) "
        "where 2^p - 1 is a Mersenne prime. It is unknown whether any "
        "odd perfect numbers exist."
    ),
    example=(
        "28: divisors = {1, 2, 4, 7, 14}. Sum = 1+2+4+7+14 = 28. "
        "28 equals sum of its proper divisors, so 28 is perfect."
    ),
    tier=4,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Perfect number', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Perfect_number",
    prerequisites=["division", "summation"],
))

register_atom(Atom(
    atom_type="conjecture",
    name="erdos_straus",
    content=(
        "The Erdos-Straus conjecture states that for every integer "
        "n >= 2, the fraction 4/n can be written as the sum of three "
        "unit fractions: 4/n = 1/x + 1/y + 1/z for some positive "
        "integers x, y, z. The conjecture has been verified "
        "computationally for all n up to 10^14."
    ),
    example=(
        "4/5 = 1/2 + 1/5 + 1/10. Verify: 1/2 + 1/5 + 1/10 = "
        "5/10 + 2/10 + 1/10 = 8/10 = 4/5."
    ),
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Erdos-Straus conjecture', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Straus_conjecture",
    prerequisites=["fraction_arithmetic"],
))

register_atom(Atom(
    atom_type="conjecture",
    name="legendre_prime",
    content=(
        "Legendre's conjecture states that there is always a prime "
        "number between n^2 and (n+1)^2 for every positive integer n. "
        "This is a stronger statement than Bertrand's postulate (which "
        "guarantees a prime between n and 2n). The conjecture remains "
        "unproven but has been verified for large ranges."
    ),
    example=(
        "n=4: search [16, 25]. 17 is prime and 16 < 17 < 25, "
        "confirming Legendre's conjecture for n=4."
    ),
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Legendre's conjecture', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Legendre%27s_conjecture",
    prerequisites=["primality", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="waring_representation",
    content=(
        "Waring's problem asks whether, for every natural number k, "
        "there exists a number s such that every natural number can "
        "be expressed as the sum of at most s k-th powers. Lagrange's "
        "four-square theorem (k=2, s=4) was the first result. For "
        "cubes (k=3), Waring's problem requires s=9. The function "
        "g(k) gives the minimum s for exponent k."
    ),
    example=(
        "Express 23 as sum of squares (k=2): 23 = 9 + 9 + 4 + 1 "
        "= 3^2 + 3^2 + 2^2 + 1^2 (4 squares)."
    ),
    tier=5,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Waring's problem', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Waring%27s_problem",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="conjecture",
    name="abc_triple",
    content=(
        "The ABC conjecture relates the radical (product of distinct "
        "prime factors) of three coprime positive integers a, b, c "
        "satisfying a + b = c. It states that for every epsilon > 0, "
        "there are only finitely many ABC triples where "
        "c > rad(abc)^{1+epsilon}. The quality q of a triple is "
        "q = log(c) / log(rad(abc)); the conjecture asserts q < 1 + "
        "epsilon for all but finitely many triples."
    ),
    example=(
        "a=1, b=8, c=9: a+b=c. rad(1*8*9) = rad(72) = 2*3 = 6. "
        "quality = log(9)/log(6) = 0.954/0.778 = 1.226. "
        "This is an ABC triple with q > 1."
    ),
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'abc conjecture', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Abc_conjecture",
    prerequisites=["gcd", "factorisation"],
))

register_atom(Atom(
    atom_type="conjecture",
    name="beal_check",
    content=(
        "Beal's conjecture states that if A^x + B^y = C^z, where "
        "A, B, C, x, y, z are positive integers with x, y, z >= 3, "
        "then A, B, and C must share a common prime factor. A prize "
        "of $1,000,000 is offered for a proof or counterexample. "
        "The task is to verify whether a given triple satisfies "
        "the equation and whether gcd(A,B,C) > 1."
    ),
    example=(
        "A=3, x=3, B=6, y=3, C=3, z=5: 27 + 216 = 243. "
        "3^3 + 6^3 = 3^5 -> 27 + 216 = 243. True. "
        "gcd(3,6,3) = 3 > 1. Consistent with Beal's conjecture."
    ),
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Beal conjecture', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Beal_conjecture",
    prerequisites=["exponentiation", "gcd"],
))

register_atom(Atom(
    atom_type="conjecture",
    name="brocard_check",
    content=(
        "Brocard's problem asks for integer solutions to n! + 1 = m^2. "
        "The only known solutions are n = 4 (4!+1 = 25 = 5^2), "
        "n = 5 (5!+1 = 121 = 11^2), and n = 7 (7!+1 = 5041 = 71^2). "
        "It is conjectured that no other solutions exist. Computational "
        "searches have verified this up to n = 10^9."
    ),
    example=(
        "n=5: 5! + 1 = 120 + 1 = 121. sqrt(121) = 11, which is an "
        "integer. So (5, 11) is a Brocard pair."
    ),
    tier=5,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Brocard's problem', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Brocard%27s_problem",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="definition",
    name="sat_verify",
    content=(
        "The Boolean satisfiability problem (SAT) asks whether a given "
        "Boolean formula can be made true by some assignment of truth "
        "values to its variables. SAT was the first problem proven to "
        "be NP-complete (Cook-Levin theorem, 1971). The verification "
        "variant takes a formula and an assignment and checks whether "
        "the assignment satisfies the formula. Verification is in P "
        "while solving is NP-complete."
    ),
    example=(
        "Formula: (x1 OR x2) AND (NOT x1 OR x3) AND (NOT x2 OR NOT x3). "
        "Assignment: x1=T, x2=F, x3=T. "
        "Clause 1: T OR F = T. Clause 2: F OR T = T. "
        "Clause 3: T OR F = T. All satisfied -> SATISFIABLE."
    ),
    tier=5,
    domain="computer_science",
    source=(
        "Wikipedia contributors, 'Boolean satisfiability problem', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Boolean_satisfiability_problem",
    prerequisites=["boolean_eval", "propositional_eval"],
))
