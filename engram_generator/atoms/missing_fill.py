"""Atoms for generators that were missing knowledge atoms.

Fills the 39-atom gap from the expanded generators added previously.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Tier 0 ──────────────────────────────────────────────────────────

register_atom(Atom(atom_type="definition", name="comparison",
    content="Comparison of two numbers determines their relative order: less than (<), "
    "greater than (>), or equal (=). For integers, compare digit by digit from the most "
    "significant. For decimals, align decimal points first. Comparison is transitive: "
    "if a < b and b < c, then a < c.",
    tier=0, domain="arithmetic",
    source="Wikipedia contributors, 'Inequality (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inequality_(mathematics)"))

register_atom(Atom(atom_type="definition", name="counting",
    content="Counting determines the number of elements in a finite collection by establishing "
    "a one-to-one correspondence with natural numbers. The cardinality of a set {a, b, c} is 3. "
    "Counting is the most fundamental mathematical operation.",
    tier=0, domain="arithmetic",
    source="Wikipedia contributors, 'Counting', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Counting"))

register_atom(Atom(atom_type="algorithm", name="rounding",
    content="Rounding replaces a number with an approximation having fewer significant digits. "
    "Round half up: if the digit after the rounding position is 5 or more, round up; otherwise "
    "round down. For example, 3.45 rounded to one decimal place is 3.5; 3.44 rounds to 3.4.",
    tier=0, domain="arithmetic",
    source="Wikipedia contributors, 'Rounding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rounding"))

# ── Tier 1 ──────────────────────────────────────────────────────────

register_atom(Atom(atom_type="definition", name="absolute_value",
    content="The absolute value |x| of a real number x is its distance from zero on the number "
    "line. |x| = x if x >= 0, and |x| = -x if x < 0. Properties: |ab| = |a||b|, "
    "|a + b| <= |a| + |b| (triangle inequality).",
    tier=1, domain="arithmetic",
    source="Wikipedia contributors, 'Absolute value', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Absolute_value"))

register_atom(Atom(atom_type="definition", name="floor_ceil",
    content="The floor function floor(x) returns the greatest integer <= x. The ceiling function "
    "ceil(x) returns the least integer >= x. floor(3.7) = 3, ceil(3.7) = 4. "
    "floor(-2.3) = -3, ceil(-2.3) = -2. For integers, floor(n) = ceil(n) = n.",
    tier=1, domain="arithmetic",
    source="Wikipedia contributors, 'Floor and ceiling functions', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Floor_and_ceiling_functions"))

register_atom(Atom(atom_type="algorithm", name="fraction_arithmetic",
    content="Fraction addition: a/b + c/d = (ad + bc) / bd. Multiplication: a/b * c/d = ac / bd. "
    "Division: a/b / c/d = a/b * d/c = ad / bc. Always reduce to lowest terms by dividing "
    "numerator and denominator by their GCD.",
    tier=1, domain="arithmetic",
    source="Wikipedia contributors, 'Fraction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fraction"))

register_atom(Atom(atom_type="formula", name="percentage",
    content="A percentage expresses a number as a fraction of 100: x% = x/100. "
    "To find x% of n: result = n * x / 100. To find what percentage a is of b: "
    "(a / b) * 100%. Percentage change: ((new - old) / old) * 100%.",
    example="25% of 80: 80 * 25/100 = 20. Percentage change from 50 to 65: (65-50)/50 * 100 = 30%",
    tier=1, domain="arithmetic",
    source="Wikipedia contributors, 'Percentage', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Percentage"))

register_atom(Atom(atom_type="algorithm", name="sequence_next",
    content="To find the next term in a sequence: identify the pattern (constant difference, "
    "constant ratio, polynomial, or recursive rule) from the given terms, then apply the rule "
    "to generate the next value. Common patterns: arithmetic (+d each step), geometric (*r each "
    "step), quadratic (second differences constant).",
    tier=1, domain="sequences",
    source="Wikipedia contributors, 'Sequence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Sequence"))

# ── Tier 2 ──────────────────────────────────────────────────────────

register_atom(Atom(atom_type="formula", name="arithmetic_mean",
    content="The arithmetic mean of n numbers is their sum divided by n: "
    "mean = (x1 + x2 + ... + xn) / n. It is the most common measure of central tendency. "
    "The mean minimises the sum of squared deviations from itself.",
    tier=2, domain="statistics",
    source="Wikipedia contributors, 'Arithmetic mean', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Arithmetic_mean"))

register_atom(Atom(atom_type="algorithm", name="prime_factorisation",
    content="Every integer greater than 1 can be uniquely expressed as a product of primes "
    "(Fundamental Theorem of Arithmetic). To factorise: divide by the smallest prime (2, 3, 5, ...) "
    "repeatedly until the quotient is 1. Example: 60 = 2^2 * 3 * 5.",
    tier=2, domain="number_theory",
    source="Wikipedia contributors, 'Integer factorization', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Integer_factorization"))

register_atom(Atom(atom_type="algorithm", name="square_root",
    content="The square root of a number x is the value y such that y^2 = x. For perfect squares, "
    "the root is an integer: sqrt(144) = 12. For non-perfect squares, the result is irrational. "
    "Newton's method approximates: y_{n+1} = (y_n + x/y_n) / 2.",
    tier=2, domain="arithmetic",
    source="Wikipedia contributors, 'Square root', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Square_root"))

register_atom(Atom(atom_type="formula", name="weighted_sum",
    content="A weighted sum multiplies each value by its weight and sums the products: "
    "result = w1*x1 + w2*x2 + ... + wn*xn. The weighted average divides by the sum of weights: "
    "avg = sum(wi*xi) / sum(wi). Used in GPA calculation, portfolio returns, etc.",
    tier=2, domain="statistics",
    source="Wikipedia contributors, 'Weighted arithmetic mean', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Weighted_arithmetic_mean"))

# ── Tier 3 ──────────────────────────────────────────────────────────

register_atom(Atom(atom_type="formula", name="dot_product",
    content="The dot product of vectors a = [a1,...,an] and b = [b1,...,bn] is "
    "a · b = a1*b1 + a2*b2 + ... + an*bn. Geometrically, a · b = |a| |b| cos(theta). "
    "The dot product is zero iff the vectors are orthogonal.",
    tier=3, domain="linear_algebra",
    source="Wikipedia contributors, 'Dot product', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dot_product"))

register_atom(Atom(atom_type="algorithm", name="matrix_add",
    content="Matrix addition: (A + B)_{ij} = A_{ij} + B_{ij}. Matrices must have the same "
    "dimensions. Addition is commutative (A + B = B + A) and associative. "
    "Scalar multiplication: (cA)_{ij} = c * A_{ij}.",
    tier=3, domain="linear_algebra",
    source="Wikipedia contributors, 'Matrix addition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Matrix_addition"))

register_atom(Atom(atom_type="algorithm", name="matrix_scalar",
    content="Scalar multiplication of a matrix: multiply every entry by the scalar. "
    "(cA)_{ij} = c * A_{ij}. Properties: c(A + B) = cA + cB, (c + d)A = cA + dA, "
    "c(dA) = (cd)A, 1*A = A.",
    tier=3, domain="linear_algebra",
    source="Wikipedia contributors, 'Scalar multiplication', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Scalar_multiplication"))

register_atom(Atom(atom_type="definition", name="product_notation",
    content="Product notation uses the capital pi symbol: prod_{i=1}^{n} a_i = a_1 * a_2 * ... * a_n. "
    "The factorial is a special case: n! = prod_{i=1}^{n} i. "
    "An empty product (n=0) equals 1 by convention.",
    tier=3, domain="arithmetic",
    source="Wikipedia contributors, 'Multiplication', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Multiplication#Capital_pi_notation"))

register_atom(Atom(atom_type="algorithm", name="recurrence_linear",
    content="A linear recurrence a(n) = c*a(n-1) + d defines each term from the previous one. "
    "Solution by unrolling: compute a(1), a(2), ... step by step. For the homogeneous case (d=0), "
    "a(n) = a(0) * c^n. For the general case, the closed form involves the particular solution d/(1-c).",
    tier=3, domain="sequences",
    source="Wikipedia contributors, 'Recurrence relation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Recurrence_relation"))

register_atom(Atom(atom_type="definition", name="summation",
    content="Summation notation: sum_{i=1}^{n} a_i = a_1 + a_2 + ... + a_n. "
    "Properties: sum(a_i + b_i) = sum(a_i) + sum(b_i), sum(c*a_i) = c*sum(a_i). "
    "Common sums: sum_{i=1}^{n} i = n(n+1)/2, sum_{i=1}^{n} i^2 = n(n+1)(2n+1)/6.",
    tier=3, domain="arithmetic",
    source="Wikipedia contributors, 'Summation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Summation"))

# ── Tier 4 ──────────────────────────────────────────────────────────

register_atom(Atom(atom_type="formula", name="cross_product",
    content="The cross product of 3D vectors a and b: a × b = [a2*b3 - a3*b2, a3*b1 - a1*b3, "
    "a1*b2 - a2*b1]. The result is perpendicular to both a and b. |a × b| = |a||b|sin(theta). "
    "The cross product is anti-commutative: a × b = -(b × a).",
    tier=4, domain="linear_algebra",
    source="Wikipedia contributors, 'Cross product', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cross_product",
    prerequisites=["dot_product"]))

register_atom(Atom(atom_type="formula", name="matrix_trace",
    content="The trace of a square matrix is the sum of its diagonal elements: "
    "tr(A) = A_{11} + A_{22} + ... + A_{nn}. Properties: tr(A + B) = tr(A) + tr(B), "
    "tr(cA) = c*tr(A), tr(AB) = tr(BA). The trace equals the sum of eigenvalues.",
    tier=4, domain="linear_algebra",
    source="Wikipedia contributors, 'Trace (linear algebra)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trace_(linear_algebra)"))

register_atom(Atom(atom_type="algorithm", name="matrix_transpose",
    content="The transpose A^T of matrix A swaps rows and columns: (A^T)_{ij} = A_{ji}. "
    "Properties: (A^T)^T = A, (A+B)^T = A^T + B^T, (AB)^T = B^T * A^T. "
    "A symmetric matrix satisfies A = A^T.",
    tier=4, domain="linear_algebra",
    source="Wikipedia contributors, 'Transpose', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transpose"))

register_atom(Atom(atom_type="formula", name="vector_norm",
    content="The Euclidean (L2) norm of vector v = [v1,...,vn] is ||v|| = sqrt(v1^2 + ... + vn^2). "
    "The L1 norm (Manhattan): ||v||_1 = |v1| + ... + |vn|. "
    "A unit vector has norm 1: v_hat = v / ||v||.",
    tier=4, domain="linear_algebra",
    source="Wikipedia contributors, 'Norm (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Norm_(mathematics)",
    prerequisites=["dot_product"]))

# ── Tier 5 ──────────────────────────────────────────────────────────

register_atom(Atom(atom_type="theorem", name="area_under_curve",
    content="The definite integral of f(x) from a to b gives the signed area under the curve: "
    "integral_a^b f(x) dx = F(b) - F(a) where F is any antiderivative of f. "
    "Positive above x-axis, negative below. The Fundamental Theorem of Calculus connects "
    "differentiation and integration.",
    tier=5, domain="calculus",
    source="Wikipedia contributors, 'Integral', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Integral",
    prerequisites=["integral"]))

register_atom(Atom(atom_type="algorithm", name="implicit_diff",
    content="Implicit differentiation finds dy/dx when y is not isolated. Differentiate both "
    "sides with respect to x, applying the chain rule to y terms (multiply by dy/dx), then "
    "solve for dy/dx. For x^2 + y^2 = r^2: 2x + 2y(dy/dx) = 0, so dy/dx = -x/y.",
    tier=5, domain="calculus",
    source="Wikipedia contributors, 'Implicit function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Implicit_function",
    prerequisites=["derivative", "chain_rule"]))

register_atom(Atom(atom_type="definition", name="logarithm",
    content="The logarithm log_b(x) is the exponent to which base b must be raised to get x: "
    "if b^y = x then log_b(x) = y. Properties: log(ab) = log(a) + log(b), "
    "log(a/b) = log(a) - log(b), log(a^n) = n*log(a). Natural log: ln(x) = log_e(x).",
    tier=5, domain="arithmetic",
    source="Wikipedia contributors, 'Logarithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Logarithm"))

register_atom(Atom(atom_type="algorithm", name="related_rates",
    content="Related rates problems involve finding the rate of change of one quantity from "
    "known rates of other related quantities. Method: (1) identify variables and rates, "
    "(2) write an equation relating the variables, (3) differentiate both sides with respect "
    "to time using the chain rule, (4) substitute known values and solve.",
    tier=5, domain="calculus",
    source="Wikipedia contributors, 'Related rates', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Related_rates",
    prerequisites=["implicit_diff"]))

# ── Tier 6 ──────────────────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="conv_2d",
    content="2D convolution slides a kernel over an input matrix, computing element-wise "
    "products and summing at each position: (I * K)_{ij} = sum_{m,n} I_{i+m,j+n} * K_{m,n}. "
    "Output size with stride 1: (H - kH + 1) × (W - kW + 1). With padding p: (H + 2p - kH + 1).",
    tier=6, domain="computer_science",
    source="Wikipedia contributors, 'Convolution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convolution",
    prerequisites=["matrix_multiply"]))

register_atom(Atom(atom_type="algorithm", name="matrix_power",
    content="Matrix power A^n = A * A * ... * A (n times). A^0 = I (identity). "
    "For diagonalisable A = PDP^{-1}: A^n = PD^nP^{-1} where D^n raises each diagonal "
    "element to the nth power. Used in Markov chains, Fibonacci via matrix exponentiation.",
    tier=6, domain="linear_algebra",
    source="Wikipedia contributors, 'Matrix exponential', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Matrix_exponential",
    prerequisites=["matrix_multiply", "eigenvalue"]))

register_atom(Atom(atom_type="algorithm", name="partial_deriv_multi",
    content="For f(x,y,...), the partial derivative df/dx treats all variables except x as "
    "constants. Mixed partials: d^2f/dxdy. Clairaut's theorem: if mixed partials are "
    "continuous, d^2f/dxdy = d^2f/dydx. The gradient is the vector of all first partials.",
    tier=6, domain="calculus",
    source="Wikipedia contributors, 'Partial derivative', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Partial_derivative",
    prerequisites=["partial_derivative"]))

register_atom(Atom(atom_type="algorithm", name="system_ode",
    content="A system of ODEs: dx/dt = f(x,y,t), dy/dt = g(x,y,t). Solved by: "
    "(1) matrix methods if linear: X' = AX, solution X(t) = e^{At}X(0); "
    "(2) numerical methods (Euler, Runge-Kutta) for general systems; "
    "(3) substitution/elimination for simple systems.",
    tier=6, domain="calculus",
    source="Wikipedia contributors, 'System of differential equations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/System_of_differential_equations",
    prerequisites=["diff_equation", "matrix_multiply"]))

# ── Tier 7 ──────────────────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="dimensional_analysis",
    content="Dimensional analysis checks that both sides of a physical equation have the same "
    "units. Base dimensions: length [L], mass [M], time [T], current [A], temperature [K]. "
    "Example: F = ma has dimensions [M][L][T^{-2}] on both sides.",
    tier=7, domain="physics",
    source="Wikipedia contributors, 'Dimensional analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dimensional_analysis",
    prerequisites=["multiplication", "division"]))

register_atom(Atom(atom_type="algorithm", name="symmetry_detection",
    content="A function f is even if f(-x) = f(x) for all x (symmetric about y-axis). "
    "f is odd if f(-x) = -f(x) (rotational symmetry about origin). "
    "Test: substitute -x and simplify. x^2 is even, x^3 is odd, x^3 + x^2 is neither.",
    tier=7, domain="algebra",
    source="Wikipedia contributors, 'Even and odd functions', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Even_and_odd_functions",
    prerequisites=["polynomial_eval"]))

register_atom(Atom(atom_type="algorithm", name="verify_proof",
    content="Proof verification checks each step for logical validity. Common errors: "
    "wrong base case in induction, dividing by zero, assuming what is to be proved (circular), "
    "distributing operations incorrectly, invalid use of converse. "
    "A valid proof has: clear premises, each step follows from previous, conclusion matches claim.",
    tier=7, domain="logic",
    source="Wikipedia contributors, 'Mathematical proof', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mathematical_proof",
    prerequisites=["proof_by_induction", "deduction_chain"]))

# ── Tier 8 ──────────────────────────────────────────────────────────

register_atom(Atom(atom_type="definition", name="abstraction_level",
    content="Abstraction identifies the general pattern underlying a concrete problem. "
    "Shortest route between cities = shortest path in weighted graph. "
    "Maximise profit with weight limit = 0/1 knapsack. "
    "Recognising the abstract structure allows reuse of known algorithms and solutions.",
    tier=8, domain="reasoning",
    source="Wikipedia contributors, 'Abstraction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Abstraction",
    prerequisites=["isomorphism_detection"]))

register_atom(Atom(atom_type="definition", name="dual_problem",
    content="The dual of an optimisation problem transforms the original (primal) into a related "
    "problem. In linear programming, the dual swaps constraints and objectives: minimising "
    "becomes maximising. Weak duality: dual optimal <= primal optimal. Strong duality: they "
    "are equal (holds for LP under Slater's condition).",
    tier=8, domain="optimisation",
    source="Wikipedia contributors, 'Dual problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dual_problem",
    prerequisites=["problem_transformation"]))

# ── Tier 9 ──────────────────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="convergence_proof",
    content="To prove an iterative algorithm converges: (1) define a potential function that "
    "decreases each step, (2) show it is bounded below, (3) conclude by monotone convergence. "
    "For contraction mappings: if |f(x) - f(y)| <= c|x-y| with c < 1, the iteration converges "
    "to a unique fixed point.",
    tier=9, domain="analysis",
    source="Wikipedia contributors, 'Banach fixed-point theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Banach_fixed-point_theorem",
    prerequisites=["invariant_discovery"]))

register_atom(Atom(atom_type="definition", name="information_bottleneck",
    content="The information bottleneck principle compresses input X into representation T that "
    "retains maximum information about target Y while minimising information about X: "
    "min I(X;T) - beta*I(T;Y). In neural networks, layers progressively discard input details "
    "while preserving task-relevant features.",
    tier=9, domain="information_theory",
    source="Wikipedia contributors, 'Information bottleneck method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Information_bottleneck_method",
    prerequisites=["info_entropy", "complexity_comparison"]))

# ── Tier 10 ─────────────────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="bottleneck_identification",
    content="Identifying computational bottlenecks: (1) profile FLOPs per component, "
    "(2) check arithmetic intensity (FLOPs / memory bytes), (3) determine if compute-bound "
    "or memory-bound. Self-attention is O(n^2) in sequence length. Sequential iteration "
    "dependencies prevent parallelisation. Fix by reducing the bottleneck dimension or "
    "algorithm complexity.",
    tier=10, domain="architecture",
    source="Wikipedia contributors, 'Computational complexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Computational_complexity",
    prerequisites=["efficiency_analysis", "architecture_analysis"]))

register_atom(Atom(atom_type="algorithm", name="regularisation_design",
    content="Regularisation reduces overfitting by constraining the model. L2 weight decay "
    "penalises large weights. Dropout randomly zeros activations during training. "
    "Data augmentation increases effective dataset size. Early stopping halts training when "
    "validation loss increases. The choice depends on the symptom: high variance suggests "
    "stronger regularisation; high bias suggests less.",
    tier=10, domain="machine_learning",
    source="Wikipedia contributors, 'Regularization (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Regularization_(mathematics)",
    prerequisites=["loss_design", "training_diagnosis"]))
