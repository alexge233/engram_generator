"""Knowledge atoms for calculus and analysis, sourced from authoritative references.

Each atom contains the full theorem statement, definition, or formula
text taken from Wikipedia, Wolfram MathWorld, ProofWiki, or NIST DLMF,
together with a citation and URL.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# 1. Power Rule (Derivative)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="power_rule",
    content=(
        "Power Rule for Derivatives (Real Number Index): "
        "Let n be a real number. Let f: R -> R be the real function defined "
        "as f(x) = x^n. Then f is differentiable on its domain and its "
        "derivative is f'(x) = n x^{n-1}, everywhere that f(x) = x^n is "
        "defined. In Leibniz notation: d/dx(x^n) = n x^{n-1}. "
        "The rule also applies when n is a natural number, integer, or "
        "rational number, with appropriate domain restrictions. "
        "When n is a positive integer, the proof follows from the binomial "
        "theorem; for real exponents, it follows from the chain rule "
        "applied to x^n = e^{n ln x}."
    ),
    tier=2,
    domain="calculus",
    source="ProofWiki, 'Power Rule for Derivatives/Real Number Index'",
    source_url="https://proofwiki.org/wiki/Power_Rule_for_Derivatives/Real_Number_Index",
    prerequisites=["multiplication"],
))


# ---------------------------------------------------------------------------
# 2. Chain Rule
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="chain_rule",
    content=(
        "Chain Rule: If a variable z depends on the variable y, which itself "
        "depends on the variable x (that is, y and z are dependent variables), "
        "then z depends on x as well, via the intermediate variable y. In "
        "this case, the chain rule is expressed as: dz/dx = (dz/dy) * (dy/dx). "
        "More precisely, if g is differentiable at the point x and f is "
        "differentiable at the point g(x), then the composite function "
        "f o g is differentiable at x, and the derivative is "
        "(f o g)'(x) = f'(g(x)) * g'(x). "
        "In Leibniz notation, letting y = f(g(x)) and u = g(x): "
        "dy/dx = (dy/du) * (du/dx)."
    ),
    tier=5,
    domain="calculus",
    source=(
        "Wikipedia, 'Chain rule'; "
        "Wolfram MathWorld, 'Chain Rule'"
    ),
    source_url="https://en.wikipedia.org/wiki/Chain_rule",
    prerequisites=["power_rule"],
))


# ---------------------------------------------------------------------------
# 3. Product Rule
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="product_rule",
    content=(
        "Product Rule: In calculus, the product rule (or Leibniz rule) is a "
        "formula used to find the derivatives of products of two or more "
        "functions. For two functions, it may be stated in Lagrange's "
        "notation as: (u * v)' = u' * v + u * v', "
        "or in Leibniz's notation as: d(u * v) = v * du + u * dv. "
        "In the notation of differentials this is: "
        "d/dx [u(x) * v(x)] = v(x) * (du/dx) + u(x) * (dv/dx). "
        "The rule extends to products of more than two factors: "
        "(u_1 u_2 ... u_n)' = u_1' u_2 ... u_n + u_1 u_2' ... u_n "
        "+ ... + u_1 u_2 ... u_n'. "
        "The discovery of this rule is credited to Gottfried Leibniz."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Product rule'",
    source_url="https://en.wikipedia.org/wiki/Product_rule",
    prerequisites=["power_rule"],
))


# ---------------------------------------------------------------------------
# 4. Quotient Rule
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="quotient_rule",
    content=(
        "Quotient Rule: In calculus, the quotient rule is a method of finding "
        "the derivative of a function that is the ratio of two differentiable "
        "functions. Let f(x) = g(x) / h(x), where both g and h are "
        "differentiable and h(x) != 0. The quotient rule states that the "
        "derivative of f(x) is: f'(x) = (g'(x) h(x) - g(x) h'(x)) / [h(x)]^2. "
        "In short notation: (f/g)' = (f'g - fg') / g^2, "
        "wherever g is nonzero."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Quotient rule'",
    source_url="https://en.wikipedia.org/wiki/Quotient_rule",
    prerequisites=["product_rule"],
))


# ---------------------------------------------------------------------------
# 5. Fundamental Theorem of Calculus (Integration / Antiderivative)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="fundamental_theorem_of_calculus",
    content=(
        "Fundamental Theorem of Calculus: "
        "First Part: Let f be a continuous real-valued function defined on a "
        "closed interval [a, b]. Let F be the function defined, for all x "
        "in [a, b], by F(x) = int_a^x f(t) dt. Then F is uniformly "
        "continuous on [a, b] and differentiable on the open interval (a, b), "
        "and F'(x) = f(x) for all x in (a, b). "
        "Second Part (Newton-Leibniz axiom): Let f be a real-valued function "
        "on a closed interval [a, b] and F an antiderivative of f in (a, b), "
        "i.e., F is continuous on [a, b] and F'(x) = f(x) for all x in "
        "(a, b). If f is Riemann integrable on [a, b], then "
        "int_a^b f(x) dx = F(b) - F(a). "
        "The two parts together link differentiation and integration as "
        "inverse operations."
    ),
    tier=5,
    domain="calculus",
    source=(
        "Wikipedia, 'Fundamental theorem of calculus'; "
        "Wolfram MathWorld, 'Fundamental Theorems of Calculus'"
    ),
    source_url="https://en.wikipedia.org/wiki/Fundamental_theorem_of_calculus",
    prerequisites=["power_rule"],
))


# ---------------------------------------------------------------------------
# 6. Definite Integral
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="definite_integral",
    content=(
        "Definite Integral (Second Fundamental Theorem of Calculus): "
        "If f is a real-valued continuous function on the closed interval "
        "[a, b] and F is the indefinite integral (antiderivative) of f on "
        "[a, b], then int_a^b f(x) dx = F(b) - F(a). "
        "This is also known as the Newton-Leibniz formula. The definite "
        "integral represents the signed area under the curve y = f(x) from "
        "x = a to x = b. The integral satisfies linearity: "
        "int_a^b [alpha f(x) + beta g(x)] dx = alpha int_a^b f(x) dx "
        "+ beta int_a^b g(x) dx, and additivity over intervals: "
        "int_a^b f(x) dx = int_a^c f(x) dx + int_c^b f(x) dx for any "
        "c in [a, b]."
    ),
    tier=5,
    domain="calculus",
    source="Wolfram MathWorld, 'Second Fundamental Theorem of Calculus'",
    source_url="https://mathworld.wolfram.com/SecondFundamentalTheoremofCalculus.html",
    prerequisites=["fundamental_theorem_of_calculus"],
))


# ---------------------------------------------------------------------------
# 7. Second Derivative Test
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="second_derivative_test",
    content=(
        "Second Derivative Test: Suppose f(x) is a function of x that is "
        "twice differentiable at a stationary point x_0 (i.e., f'(x_0) = 0). "
        "1. If f''(x_0) > 0, then f has a local minimum at x_0. "
        "2. If f''(x_0) < 0, then f has a local maximum at x_0. "
        "3. If f''(x_0) = 0, the test is inconclusive; the point x_0 may be "
        "a local minimum, local maximum, or saddle point (inflection point). "
        "The second derivative measures the concavity of the function: "
        "f''(x) > 0 indicates the graph is concave up (convex), and "
        "f''(x) < 0 indicates the graph is concave down (concave)."
    ),
    tier=3,
    domain="calculus",
    source="Wikipedia, 'Derivative test' (Second derivative test section)",
    source_url="https://en.wikipedia.org/wiki/Derivative_test",
    prerequisites=["power_rule"],
))


# ---------------------------------------------------------------------------
# 8. Partial Derivative
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="partial_derivative",
    content=(
        "Partial Derivative: In mathematics, a partial derivative of a "
        "function of several variables is its derivative with respect to one "
        "of those variables, with the others held constant (as opposed to "
        "the total derivative, in which all variables are allowed to vary). "
        "The partial derivative of a function f(x_1, ..., x_n) with respect "
        "to the variable x_i at the point a = (a_1, ..., a_n) is defined as: "
        "df/dx_i(a) = lim_{h -> 0} [f(a_1, ..., a_{i-1}, a_i + h, "
        "a_{i+1}, ..., a_n) - f(a_1, ..., a_n)] / h "
        "= lim_{h -> 0} [f(a + h e_i) - f(a)] / h, "
        "where e_i is the unit vector of the i-th axis. "
        "Partial derivatives may be thought of as the directional derivative "
        "of the function along each coordinate axis."
    ),
    tier=4,
    domain="calculus",
    source="Wikipedia, 'Partial derivative'",
    source_url="https://en.wikipedia.org/wiki/Partial_derivative",
    prerequisites=["power_rule"],
))


# ---------------------------------------------------------------------------
# 9. Gradient
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="gradient",
    content=(
        "Gradient: In vector calculus, the gradient of a scalar-valued "
        "differentiable function f of several variables is the vector field "
        "(or vector-valued function) nabla f whose value at a point p gives "
        "the direction and the rate of fastest increase. The gradient "
        "transforms like a vector under change of basis. "
        "At the point a, the gradient is defined as the vector: "
        "nabla f(a) = (df/dx_1(a), df/dx_2(a), ..., df/dx_n(a)). "
        "In three-dimensional Cartesian coordinates: "
        "grad f = nabla f = (df/dx) i + (df/dy) j + (df/dz) k, "
        "where i, j, k are the standard unit vectors. "
        "The direction of nabla f is the direction of steepest ascent, "
        "and its magnitude |nabla f| is the rate of increase in that "
        "direction, which is the greatest absolute directional derivative."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Gradient'",
    source_url="https://en.wikipedia.org/wiki/Gradient",
    prerequisites=["partial_derivative"],
))


# ---------------------------------------------------------------------------
# 10. Divergence
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="divergence",
    content=(
        "Divergence: In vector calculus, divergence is a vector operator "
        "that operates on a vector field, producing a scalar field giving "
        "the quantity of the vector field's source at each point. More "
        "technically, the divergence represents the volume density of the "
        "outward flux of a vector field from an infinitesimal volume around "
        "a given point. "
        "In three-dimensional Cartesian coordinates, the divergence of a "
        "continuously differentiable vector field F = F_x i + F_y j + F_z k "
        "is defined as: "
        "div F = nabla . F = dF_x/dx + dF_y/dy + dF_z/dz, "
        "with the obvious generalisation to arbitrary dimensions. "
        "A point at which the divergence is positive is called a 'source' of "
        "the field, and a point at which the divergence is negative is called "
        "a 'sink'. A vector field with zero divergence everywhere is called "
        "solenoidal or incompressible."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Divergence'",
    source_url="https://en.wikipedia.org/wiki/Divergence",
    prerequisites=["partial_derivative"],
))


# ---------------------------------------------------------------------------
# 11. Taylor's Theorem
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="taylor_series",
    content=(
        "Taylor's Theorem: Let k >= 1 be an integer and let the function "
        "f: R -> R be k times differentiable at the point a in R. Then "
        "there exists a function h_k: R -> R such that "
        "f(x) = f(a) + f'(a)(x - a) + f''(a)/2! (x - a)^2 + ... "
        "+ f^{(k)}(a)/k! (x - a)^k + h_k(x)(x - a)^k, "
        "and lim_{x -> a} h_k(x) = 0. This is called the Peano form of the "
        "remainder. "
        "Lagrange form of the remainder: If f is (k+1) times differentiable "
        "on the open interval between a and x, then "
        "R_k(x) = f^{(k+1)}(xi) / (k+1)! * (x - a)^{k+1} "
        "for some real number xi between a and x. "
        "The Taylor series (when the remainder vanishes as k -> infinity) is: "
        "f(x) = sum_{n=0}^{infinity} f^{(n)}(a) / n! * (x - a)^n. "
        "The special case a = 0 is called the Maclaurin series."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Taylor's theorem'",
    source_url="https://en.wikipedia.org/wiki/Taylor%27s_theorem",
    prerequisites=["power_rule"],
))


# ---------------------------------------------------------------------------
# 12. Integration by Parts
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="integration_by_parts",
    content=(
        "Integration by Parts: In calculus, and more generally in "
        "mathematical analysis, integration by parts is a process that finds "
        "the integral of a product of functions in terms of the integral of "
        "the product of their derivative and antiderivative. "
        "The rule can be stated as: "
        "int u(x) v'(x) dx = u(x) v(x) - int u'(x) v(x) dx, "
        "or more compactly: int u dv = u v - int v du. "
        "For definite integrals: "
        "int_a^b u(x) v'(x) dx = [u(x) v(x)]_a^b - int_a^b u'(x) v(x) dx. "
        "The theorem is a consequence of the product rule for "
        "differentiation. Choosing u and dv is guided by the LIATE rule: "
        "Logarithmic, Inverse trigonometric, Algebraic, Trigonometric, "
        "Exponential (in decreasing priority for u)."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Integration by parts'",
    source_url="https://en.wikipedia.org/wiki/Integration_by_parts",
    prerequisites=["fundamental_theorem_of_calculus", "product_rule"],
))


# ---------------------------------------------------------------------------
# 13. L'Hopital's Rule
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="l_hopital_rule",
    content=(
        "L'Hopital's Rule: In calculus, l'Hopital's rule or Bernoulli's "
        "rule is a theorem which provides a technique to evaluate limits of "
        "indeterminate forms. Application of the rule often converts an "
        "indeterminate form to an expression that can be easily evaluated "
        "by substitution. "
        "General form: Suppose that f and g are differentiable on an open "
        "interval I containing c (except possibly at c), and that "
        "g'(x) != 0 for all x in I with x != c. If "
        "lim_{x -> c} f(x) = lim_{x -> c} g(x) = 0, or "
        "lim_{x -> c} |f(x)| = lim_{x -> c} |g(x)| = infinity, "
        "and lim_{x -> c} f'(x)/g'(x) exists (or is +/- infinity), then "
        "lim_{x -> c} f(x)/g(x) = lim_{x -> c} f'(x)/g'(x). "
        "The rule also applies when c is replaced by +/- infinity. The rule "
        "may be applied iteratively if the resulting limit is still "
        "indeterminate. It is named after the 17th-century French "
        "mathematician Guillaume de l'Hopital, who published it in 1696."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'L'Hopital's rule'",
    source_url="https://en.wikipedia.org/wiki/L%27H%C3%B4pital%27s_rule",
    prerequisites=["power_rule", "quotient_rule"],
))


# ---------------------------------------------------------------------------
# 14. Separable Differential Equations
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="differential_equation_separable",
    content=(
        "Separation of Variables for Ordinary Differential Equations: "
        "Separation of variables is any of several methods for solving "
        "ordinary and partial differential equations, in which algebra allows "
        "one to rewrite an equation so that each of two variables occurs on a "
        "different side of the equation. "
        "For an ODE of the form dy/dx = f(x) g(y), the variables can be "
        "separated by dividing both sides by g(y): "
        "dy / g(y) = f(x) dx. "
        "Integrating both sides: int dy/g(y) = int f(x) dx + C, "
        "where C is the constant of integration. "
        "Example: For dy/dx = k y, separating gives dy/y = k dx, and "
        "integrating yields ln|y| = k x + C, so y = A e^{k x} where "
        "A = e^C. "
        "The method applies to any equation that can be written so the "
        "left side depends only on y and the right side only on x."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Separation of variables'",
    source_url="https://en.wikipedia.org/wiki/Separation_of_variables",
    prerequisites=["fundamental_theorem_of_calculus"],
))


# ---------------------------------------------------------------------------
# 15. Laplace Transform
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="laplace_transform",
    content=(
        "Laplace Transform: In mathematics, the Laplace transform, named "
        "after Pierre-Simon Laplace, is an integral transform that converts "
        "a function of a real variable t (usually time) to a function of a "
        "complex variable s (complex angular frequency). "
        "The unilateral (one-sided) Laplace transform is defined as: "
        "L{f(t)} = F(s) = int_0^{infinity} e^{-st} f(t) dt, "
        "where s = sigma + i omega is a complex number. "
        "The transform is a linear operator: "
        "L{a f(t) + b g(t)} = a F(s) + b G(s). "
        "Common transforms: L{1} = 1/s (s > 0); "
        "L{t^n} = n! / s^{n+1} (s > 0, n = 0, 1, 2, ...); "
        "L{e^{at}} = 1/(s - a) (s > a); "
        "L{sin(bt)} = b / (s^2 + b^2); "
        "L{cos(bt)} = s / (s^2 + b^2). "
        "The Laplace transform is particularly useful for solving linear "
        "ordinary differential equations with constant coefficients."
    ),
    tier=5,
    domain="calculus",
    source=(
        "Wikipedia, 'Laplace transform'; "
        "Wolfram MathWorld, 'Laplace Transform'"
    ),
    source_url="https://en.wikipedia.org/wiki/Laplace_transform",
    prerequisites=["fundamental_theorem_of_calculus"],
))


# ---------------------------------------------------------------------------
# 16. Newton-Raphson Method
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="newton_raphson",
    content=(
        "Newton-Raphson Method: In numerical analysis, Newton's method, "
        "also known as the Newton-Raphson method, is a root-finding "
        "algorithm which produces successively better approximations to the "
        "roots (or zeroes) of a real-valued function. "
        "The method starts with a function f defined over the reals and an "
        "initial guess x_0 for a root of f. If f satisfies certain "
        "assumptions and the initial guess is close enough, then "
        "x_{n+1} = x_n - f(x_n) / f'(x_n) "
        "produces a sequence that converges to the root. "
        "The method uses the first few terms of the Taylor series of f in "
        "the vicinity of the suspected root. The algorithm converges "
        "quadratically near simple roots: the number of correct digits "
        "roughly doubles with each iteration. "
        "The method may fail to converge if the initial guess is far from "
        "the root, if f'(x_n) = 0 at any iteration, or near a local "
        "extremum or horizontal asymptote."
    ),
    tier=5,
    domain="numerical_methods",
    source=(
        "Wikipedia, 'Newton's method'; "
        "Wolfram MathWorld, 'Newton's Method'"
    ),
    source_url="https://en.wikipedia.org/wiki/Newton%27s_method",
    prerequisites=["power_rule", "taylor_series"],
))


# ---------------------------------------------------------------------------
# 17. Gaussian Elimination
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="gaussian_elimination",
    content=(
        "Gaussian Elimination: In mathematics, Gaussian elimination, also "
        "known as row reduction, is an algorithm for solving systems of "
        "linear equations. It consists of a sequence of operations performed "
        "on the corresponding matrix of coefficients. This method can also "
        "be used to compute the rank of a matrix, the determinant of a "
        "square matrix, and the inverse of an invertible matrix. "
        "The method uses three types of elementary row operations: "
        "(1) swapping two rows, (2) multiplying a row by a nonzero scalar, "
        "and (3) adding a multiple of one row to another row. "
        "Using these operations, a matrix can always be transformed into an "
        "upper triangular matrix (row echelon form), and in fact into "
        "reduced row echelon form. "
        "Forward elimination: reduce the matrix to row echelon form, "
        "producing an upper triangular system. "
        "Back substitution: solve the triangular system from the last "
        "equation upward. "
        "The algorithm has time complexity O(n^3) for an n x n matrix."
    ),
    tier=5,
    domain="linear_algebra",
    source=(
        "Wikipedia, 'Gaussian elimination'; "
        "Wolfram MathWorld, 'Gaussian Elimination'"
    ),
    source_url="https://en.wikipedia.org/wiki/Gaussian_elimination",
    prerequisites=["matrix_multiply"],
))


# ---------------------------------------------------------------------------
# 18. Series Convergence Tests
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="series_convergence",
    content=(
        "Convergence Tests for Infinite Series: "
        "Ratio Test (d'Alembert's criterion): For a series sum a_n with "
        "a_n != 0 for large n, let L = lim_{n -> infinity} |a_{n+1}/a_n|. "
        "If L < 1, the series converges absolutely. If L > 1, the series "
        "diverges. If L = 1, the test is inconclusive. "
        "Direct Comparison Test: If 0 <= a_n <= b_n for all sufficiently "
        "large n, then: if sum b_n converges, then sum a_n converges; if "
        "sum a_n diverges, then sum b_n diverges. "
        "Geometric Series: sum_{n=0}^{infinity} r^n converges to 1/(1-r) "
        "if |r| < 1 and diverges if |r| >= 1. "
        "p-Series Test: sum_{n=1}^{infinity} 1/n^p converges if and only "
        "if p > 1 (when p = 1, this is the harmonic series, which diverges). "
        "Root Test: Let L = lim sup_{n -> infinity} |a_n|^{1/n}. If L < 1, "
        "the series converges absolutely. If L > 1, the series diverges."
    ),
    tier=6,
    domain="calculus",
    source=(
        "Wikipedia, 'Ratio test'; "
        "Wikipedia, 'Direct comparison test'; "
        "Wikipedia, 'Convergence tests'"
    ),
    source_url="https://en.wikipedia.org/wiki/Ratio_test",
    prerequisites=["l_hopital_rule"],
))


# ---------------------------------------------------------------------------
# 19. Fourier Series
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="fourier_series",
    content=(
        "Fourier Series: A Fourier series is an expansion of a periodic "
        "function into a sum of trigonometric functions. The Fourier series "
        "is an example of a trigonometric series. By expressing a function "
        "as a sum of sines and cosines, many problems involving the function "
        "become easier to analyse. "
        "For a periodic function f(x) with period P, the Fourier series is: "
        "f(x) ~ a_0/2 + sum_{n=1}^{infinity} [a_n cos(2 pi n x / P) "
        "+ b_n sin(2 pi n x / P)], "
        "where the Fourier coefficients are: "
        "a_n = (2/P) int_P f(x) cos(2 pi n x / P) dx, for n >= 0, "
        "b_n = (2/P) int_P f(x) sin(2 pi n x / P) dx, for n >= 1, "
        "where the integrals are taken over any interval of length P. "
        "In complex exponential form: "
        "f(x) ~ sum_{n=-infinity}^{infinity} c_n e^{i 2 pi n x / P}, "
        "where c_n = (1/P) int_P f(x) e^{-i 2 pi n x / P} dx. "
        "Convergence conditions are given by the Dirichlet conditions."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Fourier series'",
    source_url="https://en.wikipedia.org/wiki/Fourier_series",
    prerequisites=["definite_integral"],
))


# ---------------------------------------------------------------------------
# 20. Continued Fractions
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="continued_fraction",
    content=(
        "Continued Fraction: In mathematics, a continued fraction is an "
        "expression obtained through an iterative process of representing a "
        "number as the sum of its integer part and the reciprocal of another "
        "number, then writing this other number as the sum of its integer "
        "part and another reciprocal, and so on. "
        "A (generalised) continued fraction is an expression of the form: "
        "b_0 + a_1 / (b_1 + a_2 / (b_2 + a_3 / (b_3 + ...))), "
        "where a_i and b_i are called the partial numerators and partial "
        "denominators respectively. A simple (regular) continued fraction "
        "has all a_i = 1. "
        "The successive convergents x_n = A_n / B_n of the continued "
        "fraction are formed by the fundamental recurrence formulas: "
        "A_n = b_n A_{n-1} + a_n A_{n-2}, "
        "B_n = b_n B_{n-1} + a_n B_{n-2}, for n >= 1, "
        "with initial values A_{-1} = 1, A_0 = b_0, B_{-1} = 0, B_0 = 1. "
        "Every rational number has a finite simple continued fraction. "
        "Every irrational number has a unique infinite simple continued "
        "fraction. Quadratic irrationals have eventually periodic continued "
        "fraction expansions (Lagrange's theorem)."
    ),
    tier=6,
    domain="number_theory",
    source="Wikipedia, 'Continued fraction'",
    source_url="https://en.wikipedia.org/wiki/Continued_fraction",
    prerequisites=["division", "gcd"],
))


# ---------------------------------------------------------------------------
# 21. Lagrange Multipliers
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="lagrange_multipliers",
    content=(
        "Lagrange Multipliers: In mathematical optimisation, the method of "
        "Lagrange multipliers is a strategy for finding the local maxima and "
        "minima of a function subject to equation constraints. "
        "Statement: Let f and g be functions with continuous first partial "
        "derivatives on an open set containing the constraint surface "
        "g(x_1, ..., x_n) = 0, and suppose nabla g != 0 at any point on "
        "this surface. If f has a local extremum on the constraint surface "
        "at a point p, then there exists a scalar lambda (the Lagrange "
        "multiplier) such that: nabla f(p) = lambda nabla g(p). "
        "Equivalently, the gradients of f and g are parallel at constrained "
        "extrema. The method constructs the Lagrangian function "
        "L(x_1, ..., x_n, lambda) = f(x_1, ..., x_n) "
        "- lambda (g(x_1, ..., x_n) - c), "
        "and the critical points of L identify the constrained extrema. "
        "Setting nabla L = 0 gives a system of (n + 1) equations in "
        "(n + 1) unknowns: df/dx_i = lambda dg/dx_i for i = 1, ..., n "
        "and g(x) = c. "
        "The method generalises to multiple constraints via the "
        "Karush-Kuhn-Tucker conditions."
    ),
    tier=7,
    domain="calculus",
    source=(
        "Wikipedia, 'Lagrange multiplier'; "
        "Wolfram MathWorld, 'Lagrange Multiplier'"
    ),
    source_url="https://en.wikipedia.org/wiki/Lagrange_multiplier",
    prerequisites=["gradient"],
))


# ---------------------------------------------------------------------------
# 22. Euler-Lagrange Equation
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="euler_lagrange",
    content=(
        "Euler-Lagrange Equation: In the calculus of variations and "
        "classical mechanics, the Euler-Lagrange equations are a system of "
        "second-order ordinary differential equations whose solutions are "
        "stationary points of the given action functional. "
        "Statement: Given a functional of the form "
        "I[y] = int_{x_1}^{x_2} L(x, y(x), y'(x)) dx, "
        "where y(x) is a continuously differentiable function with fixed "
        "boundary values y(x_1) = y_1 and y(x_2) = y_2, a necessary "
        "condition for I[y] to have an extremum is that y satisfies the "
        "Euler-Lagrange equation: "
        "dL/dy - d/dx (dL/dy') = 0, "
        "where dL/dy denotes the partial derivative of L with respect to y, "
        "and dL/dy' denotes the partial derivative of L with respect to y'. "
        "This is analogous to Fermat's theorem in calculus (at any local "
        "extremum of a differentiable function, the derivative is zero). "
        "The equations were discovered in the 1750s by Leonhard Euler and "
        "Joseph-Louis Lagrange."
    ),
    tier=7,
    domain="calculus",
    source=(
        "Wikipedia, 'Euler-Lagrange equation'; "
        "Wolfram MathWorld, 'Euler-Lagrange Differential Equation'"
    ),
    source_url="https://en.wikipedia.org/wiki/Euler%E2%80%93Lagrange_equation",
    prerequisites=["partial_derivative", "fundamental_theorem_of_calculus"],
))
