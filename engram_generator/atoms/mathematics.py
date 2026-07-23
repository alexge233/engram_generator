"""Knowledge atoms for mathematics generators across all tiers.

Registers theorems, definitions, formulas, identities, and algorithms
for pure mathematics: arithmetic, algebra, calculus, number theory,
linear algebra, dynamic programming, combinatorics, cryptography,
signal processing, and the new extended math generators.

Physics, statistics, probability, quantum, CS, and reasoning atoms
are registered in atoms/science.py and atoms/reasoning.py respectively.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Tier 0 — Foundational Arithmetic
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="addition",
    content=(
        "In elementary arithmetic, a carry is a digit that is transferred "
        "from one column of digits to another column of more significant "
        "digits. It is part of the standard algorithm to add numbers "
        "together by starting with the rightmost digits and working to "
        "the left. When the result of an addition exceeds the value of a "
        "digit, the procedure is to 'carry' the excess amount divided by "
        "the radix to the left, adding it to the next positional value. "
        "The standard algorithm for adding multidigit numbers is to align "
        "the addends vertically and add the columns, starting from the "
        "ones column on the right. If a column's sum exceeds nine, the "
        "extra digit is 'carried' into the next column. For example, "
        "when 6 and 7 are added to make 13, the '3' is written to the "
        "same column and the '1' is carried to the left."
    ),
    tier=0,
    domain="arithmetic",
    source=(
        "Wikipedia contributors, 'Carry (arithmetic)', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Carry_(arithmetic)",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="subtraction",
    content=(
        "In the borrowing method (decomposition algorithm), each digit of "
        "the subtrahend is subtracted from the digit above it starting "
        "from right to left. If the top number is too small to subtract "
        "the bottom number from it, we add 10 to it; this 10 is "
        "'borrowed' from the top digit to the left, which is then "
        "reduced by 1. For example, to compute 932 - 457: in the ones "
        "column, 2 < 7, so we borrow 1 from the tens column (making the "
        "ones digit 12) and compute 12 - 7 = 5; the tens column becomes "
        "2 (reduced from 3), and since 2 < 5, we borrow from the "
        "hundreds column, giving 12 - 5 = 7; finally the hundreds "
        "column becomes 8 (reduced from 9), and 8 - 4 = 4, yielding "
        "475. The method processes each digit position from least "
        "significant to most significant, propagating borrows leftward."
    ),
    tier=0,
    domain="arithmetic",
    source=(
        "Wikipedia contributors, 'Subtraction', Wikipedia, "
        "The Free Encyclopedia, section 'The borrowing method'."
    ),
    source_url="https://en.wikipedia.org/wiki/Subtraction",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="sorting",
    content=(
        "Selection sort: for each position i from 0 to n-1, find the "
        "minimum element in the unsorted portion [i, n), swap it with "
        "position i. Time complexity O(n^2)."
    ),
    tier=0,
    domain="arithmetic",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="digit_root",
    content=(
        "Repeated digit summation: sum all digits of a number; if the "
        "result has more than one digit, repeat. The digit root equals "
        "n mod 9, with 9 when n mod 9 = 0 and n > 0."
    ),
    tier=0,
    domain="arithmetic",
    prerequisites=[],
))

# ---------------------------------------------------------------------------
# Tier 1 — Basic Operations and Patterns
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="multiplication",
    content=(
        "Long multiplication is the standard algorithm for multiplying "
        "larger numbers by hand in base 10. If a positional numeral "
        "system is used, a natural way of multiplying numbers is taught "
        "in schools as long multiplication: multiply the multiplicand by "
        "each digit of the multiplier, shifting each successive partial "
        "product one position to the left, and then add all the partial "
        "products together. To multiply two numbers with n and m digits, "
        "one forms n partial products, each of which is computed by "
        "multiplying the multiplicand by a single digit of the "
        "multiplier and shifting the result by the appropriate number of "
        "positions. The partial products are then summed to produce the "
        "final result. The algorithm requires at most n*m single-digit "
        "multiplications."
    ),
    tier=1,
    domain="arithmetic",
    source=(
        "Wikipedia contributors, 'Multiplication algorithm', Wikipedia, "
        "The Free Encyclopedia, section 'Long multiplication'."
    ),
    source_url="https://en.wikipedia.org/wiki/Multiplication_algorithm",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="division",
    content=(
        "Long division is a standard division algorithm suitable for "
        "dividing multi-digit Hindu-Arabic numerals. The process begins "
        "by dividing the left-most digit of the dividend by the divisor; "
        "the quotient (rounded down to an integer) becomes the first "
        "digit of the result, and the remainder is carried forward when "
        "the process is repeated on the following digit. The algorithm "
        "shifts gradually from the left to the right end of the "
        "dividend, subtracting the largest possible multiple of the "
        "divisor at each stage; the multiples then become the digits of "
        "the quotient, and the final difference is then the remainder. "
        "By the Euclidean division theorem, given two integers a (the "
        "dividend) and b (the divisor) with b != 0, there exist unique "
        "integers q (the quotient) and r (the remainder) such that "
        "a = bq + r and 0 <= r < |b|."
    ),
    tier=1,
    domain="arithmetic",
    source=(
        "Wikipedia contributors, 'Long division' and 'Euclidean "
        "division', Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Long_division",
    prerequisites=["multiplication", "subtraction"],
))

register_atom(Atom(
    atom_type="definition",
    name="fibonacci",
    content=(
        "In mathematics, the Fibonacci sequence is a sequence in which "
        "each number is the sum of the two preceding ones. The sequence "
        "commonly starts from 0 and 1, and the first few values are: "
        "0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ... The "
        "Fibonacci numbers are defined by the recurrence relation "
        "F_0 = 0, F_1 = 1, and F_n = F_{n-1} + F_{n-2} for n > 1. "
        "Like every sequence defined by a homogeneous linear recurrence "
        "with constant coefficients, the Fibonacci numbers have a "
        "closed-form expression known as Binet's formula: "
        "F_n = (phi^n - psi^n) / (phi - psi) = (phi^n - psi^n) / "
        "sqrt(5), where phi = (1 + sqrt(5))/2 (the golden ratio, "
        "approximately 1.61803) and psi = (1 - sqrt(5))/2 "
        "(approximately -0.61803). Since |psi^n / sqrt(5)| < 1/2 for "
        "all n >= 0, F_n is the nearest integer to phi^n / sqrt(5)."
    ),
    tier=1,
    domain="arithmetic",
    source=(
        "Wikipedia contributors, 'Fibonacci sequence', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Fibonacci_sequence",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="caesar",
    content=(
        "Caesar cipher: shift each letter by k positions in the alphabet. "
        "E(x) = (x + k) mod 26, D(x) = (x - k) mod 26."
    ),
    tier=1,
    domain="cryptography",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="run_length",
    content=(
        "Run-length encoding: replace consecutive identical characters with "
        "the character followed by its count. E.g., AAABBC -> A3B2C1."
    ),
    tier=1,
    domain="compression",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="theorem",
    name="linear_equation",
    content=(
        "A linear equation in one variable is an equation that can be "
        "written in the form ax + b = 0, where a and b are real numbers "
        "and a != 0. The solution is x = -b/a. More generally, the "
        "equation ax + b = c is solved by subtracting b from both sides "
        "to obtain ax = c - b, then dividing both sides by a (assuming "
        "a != 0) to give the unique solution x = (c - b)/a. If a = 0 "
        "and b = c, every real number is a solution; if a = 0 and "
        "b != c, there is no solution. A linear equation in one "
        "variable is called 'linear' because its graph (the set of "
        "solutions of a related two-variable equation y = ax + b) forms "
        "a straight line in the Cartesian plane."
    ),
    tier=1,
    domain="algebra",
    source=(
        "Wikipedia contributors, 'Linear equation', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Linear_equation",
    prerequisites=["division", "subtraction"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="expression_simplify",
    content=(
        "In mathematics, like terms are summands in a sum that differ "
        "only by a numerical factor. Like terms can be regrouped by "
        "adding their coefficients. More specifically, in a polynomial "
        "expression, like terms are those that contain the same "
        "variables raised to the same powers, possibly with different "
        "coefficients. To combine like terms, one adds the coefficients "
        "while keeping the variable part unchanged. For example, "
        "3x^2 + 5x - 2x^2 + 7x simplifies to (3 - 2)x^2 + (5 + 7)x "
        "= x^2 + 12x. An expression is considered simplified when all "
        "like terms have been combined, and all remaining terms are "
        "unlike. Simplification is employed to replace a mathematical "
        "expression with an equivalent simpler one."
    ),
    tier=1,
    domain="algebra",
    source=(
        "Wikipedia contributors, 'Like terms', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Like_terms",
    prerequisites=["addition", "multiplication"],
))

# ---------------------------------------------------------------------------
# Tier 2 — Intermediate Algebra and Calculus Introduction
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="modular",
    content=(
        "In mathematics, modular arithmetic is a system of arithmetic "
        "for certain equivalence classes of integers, called congruence "
        "classes. Sometimes it is called 'clock arithmetic', in which "
        "numbers 'wrap around' upon reaching a certain value, the "
        "modulus. Given an integer n > 1, called a modulus, two integers "
        "a and b are said to be congruent modulo n, written "
        "a \\equiv b (mod n), if n is a divisor of their difference; "
        "that is, if there is an integer k such that a - b = kn. "
        "The number n is called the modulus of the congruence. The "
        "congruence relation is an equivalence relation that is "
        "compatible with the operations of addition and multiplication; "
        "that is, if a_1 \\equiv b_1 (mod n) and a_2 \\equiv b_2 "
        "(mod n), then a_1 + a_2 \\equiv b_1 + b_2 (mod n) and "
        "a_1 * a_2 \\equiv b_1 * b_2 (mod n)."
    ),
    tier=2,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Modular arithmetic', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Modular_arithmetic",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="definition",
    name="exponentiation",
    content=(
        "Exponentiation is a mathematical operation, written as b^n, "
        "involving two numbers: the base, b, and the exponent or power, "
        "n. When n is a positive integer, exponentiation corresponds to "
        "repeated multiplication of the base: b^n is the product of "
        "multiplying n bases: b^n = b * b * ... * b (n times). "
        "The following identities, often called exponent rules, hold "
        "for all integer exponents, provided that the base is non-zero: "
        "b^{m+n} = b^m * b^n (product of powers); "
        "(b^m)^n = b^{mn} (power of a power); "
        "(b*c)^n = b^n * c^n (power of a product); "
        "b^{m-n} = b^m / b^n (quotient of powers); "
        "b^0 = 1 (zero exponent); "
        "b^{-n} = 1 / b^n (negative exponent)."
    ),
    tier=2,
    domain="arithmetic",
    source=(
        "Wikipedia contributors, 'Exponentiation', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Exponentiation",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="gcd",
    content=(
        "In mathematics, the greatest common divisor (GCD) of two or "
        "more integers, which are not all zero, is the largest positive "
        "integer that divides each of the integers. The Euclidean "
        "algorithm is an efficient method for computing the greatest "
        "common divisor, the largest number that divides both of two "
        "given numbers without leaving a remainder. It is based on the "
        "principle that the greatest common divisor of two numbers does "
        "not change if the larger number is replaced by its difference "
        "with the smaller number. The algorithm proceeds by the "
        "recurrence gcd(a, b) = gcd(b, a mod b), with the base case "
        "gcd(a, 0) = a. Since the remainders decrease with every step "
        "but can never be negative, a remainder r_N must eventually "
        "equal zero, at which point the algorithm stops. The last "
        "nonzero remainder is the greatest common divisor. The number "
        "of steps is at most five times the number of digits (in base "
        "10) of the smaller number, so the algorithm terminates in "
        "O(log(min(a, b))) steps."
    ),
    tier=2,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Euclidean algorithm' and 'Greatest "
        "common divisor', Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Euclidean_algorithm",
    prerequisites=["modular"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="polynomial_eval",
    content=(
        "In mathematics and computer science, Horner's method (or "
        "Horner's scheme) is an algorithm for polynomial evaluation. "
        "It involves rewriting a polynomial in nested form: "
        "a_0 + a_1 x + a_2 x^2 + a_3 x^3 + ... + a_n x^n "
        "= a_0 + x(a_1 + x(a_2 + x(a_3 + ... + x(a_{n-1} + "
        "x * a_n)...))). This allows the evaluation of a polynomial "
        "of degree n with only n multiplications and n additions, and "
        "this is optimal, since it is proven that no general algorithm "
        "can evaluate an arbitrary polynomial of degree n with fewer "
        "arithmetic operations when both x and the coefficients are "
        "given as input. The method is named after William George "
        "Horner, although it was known to Isaac Newton and used by "
        "Chinese mathematicians centuries earlier."
    ),
    tier=2,
    domain="algebra",
    source=(
        "Wikipedia contributors, 'Horner\\'s method', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Horner%27s_method",
    prerequisites=["multiplication", "addition"],
))

register_atom(Atom(
    atom_type="theorem",
    name="derivative",
    content=(
        "Power rule for differentiation: d/dx [a x^n] = a n x^{n-1}. "
        "The derivative of a constant is 0."
    ),
    tier=2,
    domain="calculus",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="theorem",
    name="quadratic",
    content=(
        "In algebra, a quadratic equation is any equation that can be "
        "rearranged in standard form as ax^2 + bx + c = 0, where x "
        "represents an unknown value, a, b, and c represent known "
        "numbers, and a != 0. The quadratic formula gives the solutions "
        "of this equation as x = (-b +/- sqrt(b^2 - 4ac)) / (2a). "
        "The standard way to derive this formula is to apply the method "
        "of completing the square: divide by a, rearrange, add "
        "(b/(2a))^2 to both sides, factor the left side as a perfect "
        "square, and take square roots. The quantity D = b^2 - 4ac is "
        "called the discriminant. If D > 0 there are two distinct real "
        "roots; if D = 0 there is exactly one (repeated) real root "
        "x = -b/(2a); if D < 0 there are two complex conjugate roots."
    ),
    tier=2,
    domain="algebra",
    source=(
        "Wikipedia contributors, 'Quadratic formula' and 'Quadratic "
        "equation', Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Quadratic_formula",
    prerequisites=["exponentiation", "subtraction"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="graph_reach",
    content=(
        "BFS/DFS graph reachability: from a source vertex, explore all "
        "adjacent vertices, marking each as visited. A vertex is reachable "
        "iff it is visited when the search terminates."
    ),
    tier=2,
    domain="graph_theory",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="theorem",
    name="binomial",
    content=(
        "In mathematics, the binomial coefficient C(n, k), read as "
        "'n choose k', is the number of ways to choose an (unordered) "
        "subset of k elements from a fixed set of n elements. It is "
        "given by the formula C(n, k) = n! / (k! (n - k)!) for "
        "0 <= k <= n, and C(n, k) = 0 when k > n or k < 0. "
        "Equivalently, C(n, k) = n(n-1)(n-2)...(n-k+1) / k!, which "
        "has k factors in both the numerator and denominator. The "
        "binomial coefficient satisfies Pascal's rule: "
        "C(n, k) = C(n-1, k-1) + C(n-1, k), with boundary conditions "
        "C(n, 0) = C(n, n) = 1. The name 'binomial coefficient' "
        "arises because these numbers appear as coefficients in the "
        "binomial theorem: (x + y)^n = sum_{k=0}^{n} C(n, k) "
        "x^{n-k} y^k."
    ),
    tier=2,
    domain="combinatorics",
    source=(
        "Wikipedia contributors, 'Binomial coefficient', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Binomial_coefficient",
    prerequisites=["multiplication", "division"],
))

# ---------------------------------------------------------------------------
# Tier 3 — Number Theory, Integration, Linear Algebra Intro
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="lcm",
    content=(
        "In arithmetic and number theory, the least common multiple "
        "(LCM) of two integers a and b, usually denoted by lcm(a, b), "
        "is the smallest positive integer that is divisible by both a "
        "and b. The LCM of two integers that are not both zero can be "
        "computed from their greatest common divisor by the formula: "
        "lcm(a, b) = |a * b| / gcd(a, b). This formula is also valid "
        "when exactly one of a and b is zero, since gcd(a, 0) = |a|. "
        "Using prime factorisations, if a = p_1^{e_1} * ... * p_k^{e_k} "
        "and b = p_1^{f_1} * ... * p_k^{f_k} (where exponents may be "
        "zero), then lcm(a, b) = p_1^{max(e_1,f_1)} * ... * "
        "p_k^{max(e_k,f_k)}, and dually gcd(a, b) = "
        "p_1^{min(e_1,f_1)} * ... * p_k^{min(e_k,f_k)}."
    ),
    tier=3,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Least common multiple', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Least_common_multiple",
    prerequisites=["gcd", "multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="mod_pow",
    content=(
        "Modular exponentiation is exponentiation performed over a "
        "modulus. It is useful in computer science, especially in the "
        "field of public-key cryptography. It can be computed "
        "efficiently using the method of exponentiation by squaring "
        "(also known as binary exponentiation or square-and-multiply). "
        "The method requires that the exponent e be converted to binary "
        "notation, say e = (e_{k-1} ... e_1 e_0)_2. The algorithm "
        "initialises result = 1, then for each bit from the most "
        "significant to the least significant: square the result "
        "modulo m (result = result^2 mod m), and if the current bit "
        "e_i is 1, multiply by the base modulo m "
        "(result = result * b mod m). After processing all bits, "
        "result = b^e mod m. This reduces the number of modular "
        "multiplications from O(e) to O(log e), and by reducing each "
        "intermediate result modulo m, it avoids arithmetic on very "
        "large numbers."
    ),
    tier=3,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Modular exponentiation' and "
        "'Exponentiation by squaring', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Modular_exponentiation",
    prerequisites=["modular", "exponentiation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="mod_inv",
    content=(
        "A modular multiplicative inverse of an integer a is an integer "
        "x such that the product ax is congruent to 1 with respect to "
        "the modulus m: a*x \\equiv 1 (mod m). A modular multiplicative "
        "inverse of a modulo m exists if and only if a and m are "
        "coprime, i.e., gcd(a, m) = 1. The multiplicative inverse "
        "x \\equiv a^{-1} (mod m) may be efficiently computed by "
        "solving Bezout's equation a*x + m*y = 1 for x and y using the "
        "extended Euclidean algorithm. The extended Euclidean algorithm "
        "computes, in addition to the greatest common divisor of "
        "integers a and b, also the coefficients of Bezout's identity, "
        "which are integers x and y such that a*x + b*y = gcd(a, b). "
        "When gcd(a, m) = 1, the coefficient x gives the modular "
        "inverse of a modulo m."
    ),
    tier=3,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Modular multiplicative inverse' and "
        "'Extended Euclidean algorithm', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url=(
        "https://en.wikipedia.org/wiki/Modular_multiplicative_inverse"
    ),
    prerequisites=["gcd", "modular"],
))

register_atom(Atom(
    atom_type="theorem",
    name="integral",
    content=(
        "Reverse power rule for integration: "
        "\\int a x^n dx = a x^{n+1} / (n+1) + C for n != -1."
    ),
    tier=3,
    domain="calculus",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="theorem",
    name="second_derivative",
    content=(
        "Second derivative: f''(x) = d/dx [f'(x)]. Apply the power rule "
        "twice. Measures concavity: f'' > 0 concave up, f'' < 0 concave down."
    ),
    tier=3,
    domain="calculus",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="theorem",
    name="system_equations",
    content=(
        "Cramer's rule is an explicit formula for the solution of a "
        "system of linear equations with as many equations as unknowns, "
        "valid whenever the system has a unique solution. It expresses "
        "the solution in terms of the determinants of the (square) "
        "coefficient matrix and of matrices obtained from it by "
        "replacing one column by the column vector of right-hand sides "
        "of the equations. For a 2x2 system a_1 x + b_1 y = c_1, "
        "a_2 x + b_2 y = c_2, the solution is "
        "x = (c_1 b_2 - c_2 b_1) / (a_1 b_2 - a_2 b_1), "
        "y = (a_1 c_2 - a_2 c_1) / (a_1 b_2 - a_2 b_1), "
        "provided the denominator D = a_1 b_2 - a_2 b_1 != 0. In "
        "general, for the system Ax = b where A is an n x n matrix, "
        "x_i = det(A_i) / det(A), where A_i is the matrix formed by "
        "replacing the i-th column of A with the column vector b. A "
        "unique solution exists if and only if det(A) != 0."
    ),
    tier=3,
    domain="algebra",
    source=(
        "Wikipedia contributors, 'Cramer\\'s rule', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Cramer%27s_rule",
    prerequisites=["linear_equation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="determinant",
    content=(
        "Determinant of a 2x2 matrix: det([[a,b],[c,d]]) = ad - bc. "
        "For 3x3, use cofactor expansion along the first row: "
        "det(A) = a_{11}C_{11} - a_{12}C_{12} + a_{13}C_{13}."
    ),
    tier=3,
    domain="linear_algebra",
    prerequisites=["multiplication", "subtraction"],
))

register_atom(Atom(
    atom_type="definition",
    name="collatz",
    content=(
        "Collatz sequence: if n is even, n -> n/2; if n is odd, "
        "n -> 3n+1. Conjecture: every positive integer eventually reaches 1."
    ),
    tier=3,
    domain="number_theory",
    prerequisites=["division", "multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="base_conversion",
    content=(
        "Base conversion by repeated division: divide the number by the "
        "target base, record remainders right to left. "
        "N = d_k b^k + ... + d_1 b + d_0."
    ),
    tier=3,
    domain="number_theory",
    prerequisites=["division", "modular"],
))

register_atom(Atom(
    atom_type="theorem",
    name="permutation",
    content=(
        "In mathematics, a k-permutation of a set S is an ordered "
        "arrangement of k distinct elements selected from S. The "
        "number of such k-permutations of an n-element set is denoted "
        "P(n, k) and is given by the falling factorial: "
        "P(n, k) = n! / (n - k)! = n(n-1)(n-2)...(n-k+1), which has "
        "k factors in the numerator. This counts the number of ways "
        "to choose an ordered sequence of k elements from a collection "
        "of n distinct items, where each element may be chosen at most "
        "once. When k = n, P(n, n) = n!, the total number of "
        "permutations of the entire set. The binomial coefficient is "
        "related by C(n, k) = P(n, k) / k!, since C(n, k) counts "
        "unordered selections while P(n, k) counts ordered ones."
    ),
    tier=3,
    domain="combinatorics",
    source=(
        "Wikipedia contributors, 'Permutation' and 'Falling and "
        "rising factorials', Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Permutation",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="prefix_scan",
    content=(
        "Prefix sum (scan): given array a, compute s[i] = sum(a[0..i]). "
        "Iteratively: s[0] = a[0], s[i] = s[i-1] + a[i]."
    ),
    tier=3,
    domain="algorithms",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="rpn",
    content=(
        "Reverse Polish Notation evaluation: scan tokens left to right. "
        "Push operands onto a stack; on operator, pop two operands, "
        "apply operator, push result."
    ),
    tier=3,
    domain="algorithms",
    prerequisites=["addition", "multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="cycle_detect",
    content=(
        "Floyd's cycle detection: use a slow pointer (1 step) and fast "
        "pointer (2 steps). If they meet, a cycle exists. Cycle length "
        "found by advancing one pointer until they meet again."
    ),
    tier=3,
    domain="algorithms",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="theorem",
    name="set_operations",
    content=(
        "Inclusion-exclusion principle: "
        "|A \\cup B| = |A| + |B| - |A \\cap B|. "
        "Generalises to n sets with alternating signs."
    ),
    tier=3,
    domain="set_theory",
    prerequisites=["addition", "subtraction"],
))

# ---------------------------------------------------------------------------
# Tier 4 — Linear Algebra, DP, Base Arithmetic
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="matrix_multiply",
    content=(
        "Matrix multiplication: C_{ij} = sum_k A_{ik} B_{kj}. "
        "For A (m x n) and B (n x p), result C is (m x p). "
        "Each element is a dot product of a row of A with a column of B."
    ),
    tier=4,
    domain="linear_algebra",
    prerequisites=["multiplication", "addition"],
))

register_atom(Atom(
    atom_type="theorem",
    name="matrix_inverse",
    content=(
        "2x2 matrix inverse: A^{-1} = (1/det(A)) * [[d, -b], [-c, a]] "
        "where A = [[a,b],[c,d]] and det(A) = ad - bc != 0."
    ),
    tier=4,
    domain="linear_algebra",
    prerequisites=["determinant"],
))

register_atom(Atom(
    atom_type="theorem",
    name="eigenvalue",
    content=(
        "Eigenvalue equation: Av = lambda v. "
        "Characteristic polynomial: det(A - lambda I) = 0. "
        "For 2x2: lambda^2 - tr(A) lambda + det(A) = 0."
    ),
    tier=4,
    domain="linear_algebra",
    prerequisites=["determinant", "quadratic"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="edit_distance",
    content=(
        "Levenshtein edit distance via DP: "
        "d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost) "
        "where cost=0 if s[i]=t[j], else 1."
    ),
    tier=4,
    domain="dynamic_programming",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="coin_change",
    content=(
        "Coin change DP: dp[0]=0, dp[i] = min(dp[i-c]+1) for each coin c "
        "where i-c >= 0. Finds minimum coins to make amount i."
    ),
    tier=4,
    domain="dynamic_programming",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="shortest_path",
    content=(
        "Dijkstra's algorithm: maintain priority queue of (distance, vertex). "
        "Pop minimum, relax all neighbors. "
        "d[v] = min(d[v], d[u] + w(u,v))."
    ),
    tier=4,
    domain="graph_theory",
    prerequisites=["addition", "graph_reach"],
))

register_atom(Atom(
    atom_type="theorem",
    name="derivative_eval",
    content=(
        "Derivative evaluation: compute f'(x) symbolically using power rule, "
        "then substitute the given x value to get f'(a)."
    ),
    tier=4,
    domain="calculus",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="theorem",
    name="partial_derivative",
    content=(
        "Partial derivative: df/dx treats all variables except x as constants. "
        "For f(x,y) = x^2 y + y^3, df/dx = 2xy, df/dy = x^2 + 3y^2."
    ),
    tier=4,
    domain="calculus",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="number_base_arithmetic",
    content=(
        "Base-b addition: for each digit position, compute sum with carry. "
        "If total >= b, write total mod b and carry total // b. "
        "Same as decimal addition but with base b instead of 10."
    ),
    tier=4,
    domain="number_theory",
    prerequisites=["addition", "base_conversion"],
))

# ---------------------------------------------------------------------------
# Tier 5 — Advanced Calculus, Transforms
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="chain_rule",
    content=(
        "Chain rule: d/dx [f(g(x))] = f'(g(x)) * g'(x). "
        "Derivative of a composition is the outer derivative evaluated "
        "at the inner function times the inner derivative."
    ),
    tier=5,
    domain="calculus",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="theorem",
    name="product_rule",
    content=(
        "Product rule: d/dx [f(x)g(x)] = f'(x)g(x) + f(x)g'(x). "
        "Derivative of a product is the sum of each factor "
        "differentiated while the other is held constant."
    ),
    tier=5,
    domain="calculus",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="theorem",
    name="definite_integral",
    content=(
        "Fundamental theorem of calculus: "
        "\\int_a^b f(x) dx = F(b) - F(a), where F is an antiderivative of f. "
        "Connects differentiation and integration."
    ),
    tier=5,
    domain="calculus",
    prerequisites=["integral"],
))

register_atom(Atom(
    atom_type="theorem",
    name="taylor_series",
    content=(
        "Taylor series: f(x) = sum_{n=0}^{infty} f^{(n)}(a) (x-a)^n / n!. "
        "Maclaurin series is the special case a=0."
    ),
    tier=5,
    domain="calculus",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="definition",
    name="gradient",
    content=(
        "Gradient: nabla f = (df/dx_1, ..., df/dx_n). "
        "Points in the direction of steepest ascent. "
        "Magnitude gives the rate of maximum increase."
    ),
    tier=5,
    domain="calculus",
    prerequisites=["partial_derivative"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="newton_raphson",
    content=(
        "Newton-Raphson method: x_{n+1} = x_n - f(x_n) / f'(x_n). "
        "Iteratively refines a root estimate. "
        "Converges quadratically near simple roots."
    ),
    tier=5,
    domain="numerical_methods",
    prerequisites=["derivative", "division"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="gaussian_elimination",
    content=(
        "Gaussian elimination: reduce augmented matrix to row echelon form "
        "using elementary row operations (swap, scale, add multiple of one "
        "row to another). Back-substitute to find solution."
    ),
    tier=5,
    domain="linear_algebra",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="theorem",
    name="laplace_transform",
    content=(
        "Laplace transform: L{f(t)} = F(s) = \\int_0^{infty} e^{-st} f(t) dt. "
        "Key transforms: L{1} = 1/s, L{t^n} = n!/s^{n+1}, "
        "L{e^{at}} = 1/(s-a)."
    ),
    tier=5,
    domain="calculus",
    prerequisites=["integral"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="vigenere",
    content=(
        "Vigenere cipher: E(m_i) = (m_i + k_{i mod len(k)}) mod 26. "
        "Polyalphabetic substitution using a repeating keyword."
    ),
    example="Plaintext 'HELLO', key 'KEY': H+K=R, E+E=I, L+Y=J, L+K=V, O+E=S. Ciphertext = 'RIJVS'",
    tier=5,
    domain="cryptography",
    prerequisites=["caesar", "modular"],
))

register_atom(Atom(
    atom_type="theorem",
    name="quotient_rule",
    content=(
        "Quotient rule: d/dx [f(x)/g(x)] = (f'g - fg') / g^2. "
        "Derivative of a quotient using the product and chain rules."
    ),
    tier=5,
    domain="calculus",
    prerequisites=["product_rule"],
))

register_atom(Atom(
    atom_type="theorem",
    name="limit",
    content=(
        "L'Hopital's rule: if lim f/g gives 0/0 or inf/inf, "
        "then lim f/g = lim f'/g'. "
        "Apply repeatedly until the indeterminate form resolves."
    ),
    tier=5,
    domain="calculus",
    prerequisites=["derivative", "division"],
))

register_atom(Atom(
    atom_type="identity",
    name="complex_division",
    content=(
        "Complex division: (a+bi)/(c+di) = ((a+bi)(c-di)) / (c^2+d^2). "
        "Multiply numerator and denominator by the conjugate of the "
        "denominator to eliminate the imaginary part in the denominator."
    ),
    tier=5,
    domain="complex_analysis",
    prerequisites=["complex_arithmetic"],
))

# ---------------------------------------------------------------------------
# Tier 6 — Number Theory, Combinatorics, Advanced DP, Advanced Math
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="totient",
    content=(
        "In number theory, Euler's totient function phi(n) counts the "
        "positive integers up to a given integer n that are relatively "
        "prime to n. In other words, it is the number of integers k in "
        "the range 1 <= k <= n for which gcd(n, k) = 1. The function "
        "is a multiplicative function, meaning that if gcd(m, n) = 1, "
        "then phi(m*n) = phi(m)*phi(n). For a prime power, "
        "phi(p^k) = p^{k-1}(p - 1) = p^k(1 - 1/p). For an arbitrary "
        "positive integer n with prime factorisation "
        "n = p_1^{k_1} * p_2^{k_2} * ... * p_r^{k_r}, "
        "phi(n) = n * prod_{p|n} (1 - 1/p) "
        "= p_1^{k_1-1}(p_1-1) * p_2^{k_2-1}(p_2-1) * ... * "
        "p_r^{k_r-1}(p_r-1), where the product is over the distinct "
        "prime factors of n. The term 'totient' was coined by "
        "J. J. Sylvester in 1879."
    ),
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Euler\\'s totient function', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url=(
        "https://en.wikipedia.org/wiki/Euler%27s_totient_function"
    ),
    prerequisites=["factorisation", "multiplication"],
))

register_atom(Atom(
    atom_type="theorem",
    name="crt",
    content=(
        "The Chinese remainder theorem states that if one knows the "
        "remainders of the Euclidean division of an integer n by "
        "several integers, then one can determine uniquely the "
        "remainder of the division of n by the product of these "
        "integers, under the condition that the divisors are pairwise "
        "coprime (no two divisors share a common factor other than 1). "
        "More precisely, if n_1, n_2, ..., n_k are pairwise coprime "
        "positive integers, and if a_1, a_2, ..., a_k are integers "
        "such that 0 <= a_i < n_i for every i, then there is one and "
        "only one integer x such that 0 <= x < N = n_1 * n_2 * ... * "
        "n_k and the remainder of the Euclidean division of x by n_i "
        "is a_i for every i. The solution is given by "
        "x = sum_{i=1}^{k} a_i * M_i * y_i (mod N), where "
        "M_i = N / n_i and y_i is the modular inverse of M_i modulo "
        "n_i, i.e., M_i * y_i \\equiv 1 (mod n_i)."
    ),
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Chinese remainder theorem', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url=(
        "https://en.wikipedia.org/wiki/Chinese_remainder_theorem"
    ),
    prerequisites=["modular", "mod_inv"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="primality",
    content=(
        "A primality test is an algorithm for determining whether an "
        "input number is prime. Trial division is the simplest of all "
        "primality tests: given an input number n, it checks whether n "
        "is divisible by any prime number between 2 and sqrt(n) "
        "(i.e., whether the division leaves no remainder). If n is "
        "divisible by any such number, it is composite; otherwise it is "
        "prime. The optimisation of only testing divisors up to "
        "sqrt(n) works because if n = a*b is composite and a <= b, "
        "then a <= sqrt(n). Therefore, if no divisor up to sqrt(n) is "
        "found, n must be prime. In practice, one checks divisibility "
        "by 2, then tests odd numbers from 3 up to sqrt(n). Every "
        "positive integer greater than 1 is divisible by at least one "
        "prime number, by the fundamental theorem of arithmetic, so "
        "it suffices to test only prime divisors."
    ),
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Primality test' and 'Trial "
        "division', Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Trial_division",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="theorem",
    name="factorisation",
    content=(
        "The fundamental theorem of arithmetic, also called the unique "
        "factorization theorem and prime factorization theorem, states "
        "that every integer greater than 1 is either a prime number "
        "itself or can be represented as the product of prime numbers "
        "and that, moreover, this representation is unique, up to "
        "(except for) the order of the factors. More formally, for "
        "every integer n > 1 there exist unique primes "
        "p_1 <= p_2 <= ... <= p_k such that n = p_1 * p_2 * ... * p_k. "
        "This may also be written as n = p_1^{a_1} * p_2^{a_2} * ... "
        "* p_r^{a_r}, where p_1 < p_2 < ... < p_r are distinct primes "
        "and the a_i are positive integers. Prime factorisation by "
        "trial division finds these factors by dividing n by each "
        "prime up to sqrt(n), recording each prime factor and its "
        "multiplicity."
    ),
    tier=6,
    domain="number_theory",
    source=(
        "Wikipedia contributors, 'Fundamental theorem of arithmetic', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url=(
        "https://en.wikipedia.org/wiki/"
        "Fundamental_theorem_of_arithmetic"
    ),
    prerequisites=["primality", "division"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="topo_sort",
    content=(
        "Topological sort (Kahn's algorithm): repeatedly remove vertices "
        "with in-degree 0, append to result. Valid only for DAGs. "
        "If result length < |V|, a cycle exists."
    ),
    tier=6,
    domain="graph_theory",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="theorem",
    name="catalan",
    content=(
        "In combinatorial mathematics, the Catalan numbers are a "
        "sequence of natural numbers that occur in various counting "
        "problems, often involving recursively defined objects. The "
        "n-th Catalan number can be expressed directly in terms of the "
        "central binomial coefficients by the closed form: "
        "C_n = (1/(n+1)) * C(2n, n) = (2n)! / ((n+1)! * n!) for "
        "n >= 0. An equivalent form is "
        "C_n = C(2n, n) - C(2n, n+1), which shows that C_n is always "
        "an integer. The Catalan numbers satisfy Segner's recurrence "
        "relation: C_0 = 1, C_{n+1} = sum_{i=0}^{n} C_i * C_{n-i} "
        "for n >= 0. The first Catalan numbers for n = 0, 1, 2, 3, "
        "4, 5, 6, 7, 8, ... are 1, 1, 2, 5, 14, 42, 132, 429, "
        "1430, ... They count, among other things, the number of "
        "expressions containing n pairs of correctly matched "
        "parentheses, the number of distinct binary search trees with "
        "n nodes, and the number of full binary trees with n + 1 "
        "leaves."
    ),
    tier=6,
    domain="combinatorics",
    source=(
        "Wikipedia contributors, 'Catalan number', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Catalan_number",
    prerequisites=["binomial"],
))

register_atom(Atom(
    atom_type="theorem",
    name="derangement",
    content=(
        "In combinatorial mathematics, a derangement is a permutation "
        "of the elements of a set in which no element appears in its "
        "original position. In other words, a derangement is a "
        "permutation that has no fixed points. The number of "
        "derangements of a set of size n is known as the subfactorial "
        "of n, denoted !n or D_n. It satisfies two recurrence "
        "relations: (1) D_n = (n-1)(D_{n-1} + D_{n-2}) for n >= 2, "
        "with D_0 = 1 and D_1 = 0; and (2) D_n = n*D_{n-1} + (-1)^n. "
        "The subfactorial also has the explicit formula using the "
        "inclusion-exclusion principle: "
        "D_n = n! * sum_{k=0}^{n} (-1)^k / k!, and for n >= 1, D_n "
        "is the nearest integer to n!/e, where e is Euler's number. "
        "The first few derangement numbers are "
        "D_0=1, D_1=0, D_2=1, D_3=2, D_4=9, D_5=44, D_6=265."
    ),
    tier=6,
    domain="combinatorics",
    source=(
        "Wikipedia contributors, 'Derangement', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Derangement",
    prerequisites=["permutation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="knapsack",
    content=(
        "0/1 Knapsack DP: dp[i][w] = max(dp[i-1][w], dp[i-1][w-w_i] + v_i). "
        "Maximise total value without exceeding weight capacity W."
    ),
    example="Capacity W=10. Items: (w=5,v=10), (w=4,v=40), (w=6,v=30). Optimal: (w=4,v=40)+(w=6,v=30) = v=70",
    tier=6,
    domain="dynamic_programming",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="lcs",
    content=(
        "Longest Common Subsequence DP: if s[i]=t[j], dp[i][j] = dp[i-1][j-1]+1; "
        "else dp[i][j] = max(dp[i-1][j], dp[i][j-1]). Backtrack to recover the LCS."
    ),
    example="X='ABCBDAB', Y='BDCAB': LCS = 'BCAB', length 4",
    tier=6,
    domain="dynamic_programming",
    prerequisites=["edit_distance"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="lis",
    content=(
        "Longest Increasing Subsequence: dp[i] = max(dp[j]+1) for j < i "
        "where a[j] < a[i]. O(n^2) DP, O(n log n) with patience sorting."
    ),
    example="Sequence [10,9,2,5,3,7,101,18]: LIS = [2,3,7,101] or [2,5,7,101], length 4",
    tier=6,
    domain="dynamic_programming",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="polynomial_multiply",
    content=(
        "To expand the product of two polynomials into a sum of terms, "
        "the distributive law is repeatedly applied, which results in "
        "each term of one polynomial being multiplied by every term of "
        "the other. For two binomials, this process is sometimes called "
        "the FOIL method (First, Outer, Inner, Last): "
        "(a + b)(c + d) = ac + ad + bc + bd. More generally, for "
        "polynomials p(x) = sum_{i=0}^{m} a_i x^i and "
        "q(x) = sum_{j=0}^{n} b_j x^j, their product is "
        "p(x)*q(x) = sum_{k=0}^{m+n} c_k x^k, where the coefficient "
        "c_k = sum_{i+j=k} a_i * b_j is the discrete convolution of "
        "the coefficient sequences. The product polynomial has degree "
        "m + n and the naive algorithm requires O(m*n) coefficient "
        "multiplications."
    ),
    tier=6,
    domain="algebra",
    source=(
        "Wikipedia contributors, 'FOIL method' and 'Polynomial', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/FOIL_method",
    prerequisites=["polynomial_eval", "multiplication"],
))

register_atom(Atom(
    atom_type="theorem",
    name="integration_by_parts",
    content=(
        "Integration by parts: \\int u dv = uv - \\int v du. "
        "Choose u as the term that simplifies when differentiated "
        "(LIATE rule: Logs, Inverse trig, Algebraic, Trig, Exponential)."
    ),
    tier=6,
    domain="calculus",
    prerequisites=["integral", "product_rule"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="partial_fractions",
    content=(
        "Partial fraction decomposition: "
        "(ax+b)/((x-r_1)(x-r_2)) = A/(x-r_1) + B/(x-r_2). "
        "Solve for A and B by the cover-up method: "
        "A = f(r_1)/(r_1-r_2), B = f(r_2)/(r_2-r_1)."
    ),
    tier=6,
    domain="calculus",
    prerequisites=["factorisation", "system_equations"],
))

register_atom(Atom(
    atom_type="theorem",
    name="series_convergence",
    content=(
        "Series convergence tests: "
        "Geometric: |r| < 1 converges, |r| >= 1 diverges. "
        "p-series: 1/n^p converges iff p > 1. "
        "Ratio test: lim |a_{n+1}/a_n| < 1 converges, > 1 diverges."
    ),
    tier=6,
    domain="calculus",
    prerequisites=["limit", "division"],
))

register_atom(Atom(
    atom_type="theorem",
    name="de_moivre",
    content=(
        "De Moivre's theorem: (r e^{i theta})^n = r^n e^{i n theta}. "
        "Equivalently: (r(cos theta + i sin theta))^n = "
        "r^n (cos(n theta) + i sin(n theta))."
    ),
    example="(cos 30 + i sin 30)^6 = cos(180) + i sin(180) = -1 + 0i = -1",
    tier=6,
    domain="complex_analysis",
    prerequisites=["complex_modulus", "exponentiation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="group_order",
    content=(
        "Order of a group element: the smallest positive integer k such that "
        "a^k \\equiv 1 (mod n). By Lagrange's theorem, k divides phi(n)."
    ),
    tier=6,
    domain="abstract_algebra",
    prerequisites=["modular", "multiplication"],
))

register_atom(Atom(
    atom_type="theorem",
    name="fourier_coefficient",
    content=(
        "Fourier series coefficients: "
        "a_n = (2/T) \\int_0^T f(t) cos(2 pi n t / T) dt, "
        "b_n = (2/T) \\int_0^T f(t) sin(2 pi n t / T) dt. "
        "Square wave b_n = 4/(n pi) for odd n, 0 for even n."
    ),
    tier=6,
    domain="signal_processing",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="definition",
    name="tensor_product",
    content=(
        "Tensor (Kronecker) product: for u in R^m, v in R^n, "
        "u \\otimes v is the mn-vector with entries u_i v_j. "
        "For 2-vectors: [a,b]^T \\otimes [c,d]^T = [ac, ad, bc, bd]^T."
    ),
    tier=6,
    domain="linear_algebra",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="identity",
    name="pauli_product",
    content=(
        "Pauli matrix algebra: sigma_x sigma_y = i sigma_z (cyclic). "
        "sigma_i^2 = I for all i. "
        "sigma_x = [[0,1],[1,0]], sigma_y = [[0,-i],[i,0]], "
        "sigma_z = [[1,0],[0,-1]]."
    ),
    tier=6,
    domain="quantum",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="bloch_coords",
    content=(
        "Bloch sphere coordinates: for |psi> = alpha|0> + beta|1>, "
        "theta = 2 arccos(|alpha|), phi = arg(beta) - arg(alpha). "
        "Maps any single-qubit pure state to a point on S^2."
    ),
    example="|psi> = cos(pi/6)|0> + e^(i*pi/4)*sin(pi/6)|1>. theta=pi/3, phi=pi/4. Bloch coords: (sin(pi/3)*cos(pi/4), sin(pi/3)*sin(pi/4), cos(pi/3)) = (0.612, 0.612, 0.5)",
    tier=6,
    domain="quantum",
    prerequisites=["complex_modulus", "euler_formula"],
))

register_atom(Atom(
    atom_type="theorem",
    name="diff_equation",
    content=(
        "Separable ODE: dy/dx = f(x)g(y). Separate: dy/g(y) = f(x)dx, "
        "integrate both sides. For dy/dx = ky: y = Ce^{kx}."
    ),
    tier=6,
    domain="calculus",
    prerequisites=["integral"],
))

register_atom(Atom(
    atom_type="theorem",
    name="divergence",
    content=(
        "Divergence of a vector field: "
        "div F = dF_x/dx + dF_y/dy + dF_z/dz. "
        "Measures the net outward flux per unit volume."
    ),
    tier=6,
    domain="calculus",
    prerequisites=["partial_derivative"],
))

register_atom(Atom(
    atom_type="theorem",
    name="quadratic_residue",
    content=(
        "Quadratic residue: a is a QR mod p if x^2 \\equiv a (mod p) "
        "has a solution. Euler's criterion: a^{(p-1)/2} \\equiv 1 (mod p) "
        "iff a is a QR."
    ),
    tier=6,
    domain="number_theory",
    prerequisites=["mod_pow", "primality"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="continued_fraction",
    content=(
        "Continued fraction expansion: a/b = q_0 + 1/(q_1 + 1/(q_2 + ...)) "
        "where q_i = floor(a_i/b_i), and (a_{i+1}, b_{i+1}) = (b_i, a_i mod b_i)."
    ),
    tier=6,
    domain="number_theory",
    prerequisites=["division", "gcd"],
))

register_atom(Atom(
    atom_type="theorem",
    name="diophantine",
    content=(
        "Linear Diophantine equation: ax + by = c has integer solutions "
        "iff gcd(a,b) | c. General solution: x = x_0 + (b/d)t, "
        "y = y_0 - (a/d)t for integer t, where d = gcd(a,b)."
    ),
    tier=6,
    domain="number_theory",
    prerequisites=["gcd", "mod_inv"],
))

register_atom(Atom(
    atom_type="theorem",
    name="recurrence_solve",
    content=(
        "Linear recurrence: a_n = c_1 a_{n-1} + c_2 a_{n-2}. "
        "Characteristic equation: r^2 = c_1 r + c_2. "
        "If roots r_1, r_2 distinct: a_n = A r_1^n + B r_2^n."
    ),
    tier=6,
    domain="algebra",
    prerequisites=["quadratic"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="polynomial_division",
    content=(
        "Synthetic division of polynomial by (x - c): bring down leading "
        "coefficient, multiply by c, add to next coefficient, repeat. "
        "Last value is the remainder."
    ),
    tier=6,
    domain="algebra",
    prerequisites=["polynomial_eval"],
))
