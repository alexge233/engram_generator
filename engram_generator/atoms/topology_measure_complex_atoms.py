"""Knowledge atoms for topology, measure theory, and complex analysis.

Registers theorem, definition, and formula atoms covering general
topology, Lebesgue measure theory, and complex function theory.
Each atom includes a worked example, Wikipedia source URL, and
prerequisite atoms.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Topology (tier 5-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="open_closed_sets",
    content=(
        "In a topological space (X, tau), a set U is open if U belongs to "
        "tau. A set F is closed if its complement X \\ F is open. In a "
        "metric space, U is open iff for every x in U there exists "
        "epsilon > 0 such that B(x, epsilon) is a subset of U. The empty "
        "set and X are both open and closed."
    ),
    example=(
        "In R with standard topology: (0,1) is open because for any "
        "x in (0,1), B(x, min(x, 1-x)) is a subset of (0,1). "
        "[0,1] is closed because R \\ [0,1] = (-inf,0) union (1,inf) "
        "is open."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Open set', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Open_set",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="closure_interior",
    content=(
        "The closure of a set A, denoted cl(A) or A-bar, is the smallest "
        "closed set containing A; equivalently, A together with all its "
        "limit points. The interior of A, denoted int(A), is the largest "
        "open set contained in A. The boundary of A is "
        "bd(A) = cl(A) \\ int(A)."
    ),
    example=(
        "A = (0,1) in R: cl(A) = [0,1], int(A) = (0,1), "
        "bd(A) = {0, 1}. For A = Q (rationals) in R: cl(Q) = R, "
        "int(Q) = empty set."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Closure (topology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Closure_(topology)",
    prerequisites=["open_closed_sets"],
))

register_atom(Atom(
    atom_type="definition",
    name="continuity_topological",
    content=(
        "A function f: X -> Y between topological spaces is continuous "
        "if the preimage f^{-1}(V) of every open set V in Y is open in X. "
        "Equivalently, the preimage of every closed set is closed. In "
        "metric spaces, this coincides with the epsilon-delta definition."
    ),
    example=(
        "f: R -> R, f(x) = x^2. For any open interval (a,b) with "
        "a >= 0: f^{-1}((a,b)) = (-sqrt(b),-sqrt(a)) union "
        "(sqrt(a),sqrt(b)), which is open. So f is continuous."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Continuous function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Continuous_function",
    prerequisites=["open_closed_sets"],
))

register_atom(Atom(
    atom_type="definition",
    name="homeomorphism_check",
    content=(
        "A homeomorphism is a bijective continuous function f: X -> Y "
        "whose inverse f^{-1} is also continuous. Two spaces are "
        "homeomorphic if a homeomorphism exists between them. "
        "Homeomorphic spaces share all topological properties "
        "(compactness, connectedness, genus, etc.)."
    ),
    example=(
        "f: (-1,1) -> R, f(x) = x/(1-x^2). f is bijective, continuous, "
        "and f^{-1} is continuous. So (-1,1) is homeomorphic to R. "
        "But [0,1] is not homeomorphic to (0,1) because [0,1] is "
        "compact while (0,1) is not."
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Homeomorphism', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Homeomorphism",
    prerequisites=["continuity_topological"],
))

register_atom(Atom(
    atom_type="formula",
    name="euler_characteristic",
    content=(
        "The Euler characteristic of a polyhedron or CW complex is "
        "chi = V - E + F, where V is the number of vertices, E edges, "
        "and F faces. For a convex polyhedron, chi = 2. For a surface "
        "of genus g, chi = 2 - 2g. The Euler characteristic is a "
        "topological invariant."
    ),
    example=(
        "Cube: V=8, E=12, F=6. chi = 8 - 12 + 6 = 2. "
        "Torus (genus 1): chi = 2 - 2(1) = 0. "
        "Tetrahedron: V=4, E=6, F=4. chi = 4 - 6 + 4 = 2."
    ),
    tier=5,
    domain="topology",
    source="Wikipedia contributors, 'Euler characteristic', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euler_characteristic",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="connected_check",
    content=(
        "A topological space X is connected if it cannot be written as "
        "the union of two disjoint non-empty open sets. Equivalently, "
        "the only sets that are both open and closed are X and the "
        "empty set. A space is path-connected if for any two points "
        "there exists a continuous path between them. Path-connected "
        "implies connected, but not conversely in general."
    ),
    example=(
        "R is connected: if R = U union V with U,V open and disjoint, "
        "one must be empty. (0,1) union (2,3) is disconnected: "
        "U = (0,1) and V = (2,3) are both open and disjoint."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Connected space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Connected_space",
    prerequisites=["open_closed_sets"],
))

register_atom(Atom(
    atom_type="definition",
    name="compactness_check",
    content=(
        "A topological space X is compact if every open cover has a "
        "finite subcover. In R^n, by the Heine-Borel theorem, a set "
        "is compact iff it is closed and bounded. Compact sets have "
        "many useful properties: continuous images of compact sets are "
        "compact, and continuous real-valued functions on compact sets "
        "attain their maximum and minimum."
    ),
    example=(
        "[0,1] is compact (closed and bounded in R). (0,1) is not "
        "compact: the cover {(1/n, 1) : n >= 1} has no finite "
        "subcover. Z (integers) is closed but not bounded, so not "
        "compact."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Compact space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Compact_space",
    prerequisites=["open_closed_sets"],
))

register_atom(Atom(
    atom_type="theorem",
    name="fixed_point_existence",
    content=(
        "The Brouwer fixed-point theorem states that every continuous "
        "function f: D^n -> D^n from a closed n-dimensional disc to "
        "itself has at least one fixed point x such that f(x) = x. "
        "The Banach fixed-point theorem states that a contraction "
        "mapping on a complete metric space has a unique fixed point."
    ),
    example=(
        "Brouwer: f: [0,1] -> [0,1], f(x) = cos(x). Since "
        "f(0) = 1 > 0 and f(1) = cos(1) ~ 0.54 < 1, by IVT on "
        "g(x) = f(x) - x, there exists x* with f(x*) = x*. "
        "Numerically x* ~ 0.7391."
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Brouwer fixed-point theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Brouwer_fixed-point_theorem",
    prerequisites=["compactness_check", "continuity_topological"],
))


# ---------------------------------------------------------------------------
# Measure Theory (tier 6-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="sigma_algebra",
    content=(
        "A sigma-algebra (sigma-field) on a set X is a collection F of "
        "subsets of X that contains X, is closed under complementation, "
        "and is closed under countable unions. The pair (X, F) is called "
        "a measurable space. The Borel sigma-algebra on R is the smallest "
        "sigma-algebra containing all open sets."
    ),
    example=(
        "On X = {1,2,3}: F = {empty, {1}, {2,3}, {1,2,3}} is a "
        "sigma-algebra. Check: X in F, complement of {1} = {2,3} in F, "
        "complement of {2,3} = {1} in F, union {1} union {2,3} = X in F."
    ),
    tier=6,
    domain="measure_theory",
    source="Wikipedia contributors, 'Sigma-algebra', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Sigma-algebra",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="measurable_function",
    content=(
        "A function f: (X, F) -> (Y, G) between measurable spaces is "
        "measurable if the preimage f^{-1}(B) belongs to F for every "
        "B in G. For real-valued functions, f is measurable iff "
        "{x : f(x) > a} is in F for every a in R."
    ),
    example=(
        "f: R -> R, f(x) = x^2. For any a > 0: {x : x^2 > a} = "
        "(-inf, -sqrt(a)) union (sqrt(a), inf), which is a Borel set. "
        "For a <= 0: {x : x^2 > a} = R. So f is Borel measurable."
    ),
    tier=6,
    domain="measure_theory",
    source="Wikipedia contributors, 'Measurable function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Measurable_function",
    prerequisites=["sigma_algebra"],
))

register_atom(Atom(
    atom_type="definition",
    name="lebesgue_measure",
    content=(
        "The Lebesgue measure on R^n extends the notion of length, area, "
        "and volume to a large class of sets. For an interval [a,b], "
        "lambda([a,b]) = b - a. The Lebesgue measure is translation "
        "invariant, countably additive, and complete. The Cantor set "
        "has Lebesgue measure zero despite being uncountable."
    ),
    example=(
        "lambda([2, 5]) = 5 - 2 = 3. "
        "lambda([0,1] union [3,4]) = 1 + 1 = 2 (disjoint union). "
        "lambda(Q intersect [0,1]) = 0 (rationals have measure zero)."
    ),
    tier=6,
    domain="measure_theory",
    source="Wikipedia contributors, 'Lebesgue measure', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lebesgue_measure",
    prerequisites=["sigma_algebra"],
))

register_atom(Atom(
    atom_type="definition",
    name="simple_function_integral",
    content=(
        "A simple function is a measurable function that takes finitely "
        "many values: s = sum(a_i * 1_{A_i}). The Lebesgue integral of "
        "a non-negative simple function is integral(s) = sum(a_i * "
        "mu(A_i)). The integral of a general non-negative measurable "
        "function is the supremum over integrals of simple functions "
        "below it."
    ),
    example=(
        "s = 2 * 1_{[0,1]} + 5 * 1_{(1,3]}. integral(s) = "
        "2 * lambda([0,1]) + 5 * lambda((1,3]) = 2*1 + 5*2 = 12."
    ),
    tier=6,
    domain="measure_theory",
    source="Wikipedia contributors, 'Lebesgue integration', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lebesgue_integration",
    prerequisites=["lebesgue_measure", "measurable_function"],
))

register_atom(Atom(
    atom_type="theorem",
    name="dominated_convergence",
    content=(
        "The Dominated Convergence Theorem (Lebesgue): if f_n -> f "
        "pointwise a.e. and |f_n| <= g for some integrable g, then "
        "f is integrable and lim integral(f_n) = integral(lim f_n) = "
        "integral(f). This allows interchange of limit and integral "
        "under a dominating function."
    ),
    example=(
        "f_n(x) = x^n on [0,1]. f_n -> 0 a.e. (except at x=1). "
        "|f_n| <= 1 = g, which is integrable on [0,1]. By DCT: "
        "lim integral(x^n dx, 0 to 1) = integral(0) = 0. "
        "Direct: integral(x^n) = 1/(n+1) -> 0. Confirmed."
    ),
    tier=7,
    domain="measure_theory",
    source="Wikipedia contributors, 'Dominated convergence theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dominated_convergence_theorem",
    prerequisites=["simple_function_integral"],
))

register_atom(Atom(
    atom_type="theorem",
    name="monotone_convergence",
    content=(
        "The Monotone Convergence Theorem (Lebesgue): if f_n is a "
        "sequence of non-negative measurable functions with "
        "f_1 <= f_2 <= ... and f_n -> f pointwise, then "
        "lim integral(f_n) = integral(f). The limit may be infinity."
    ),
    example=(
        "f_n(x) = min(x, n) on [0, inf). f_n increases to f(x) = x. "
        "integral(f_n, 0 to N) = integral(x, 0 to N) = N^2/2 for "
        "large n. So integral(f) = integral(x, 0 to inf) = infinity."
    ),
    tier=7,
    domain="measure_theory",
    source="Wikipedia contributors, 'Monotone convergence theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Monotone_convergence_theorem_(Lebesgue_integration)",
    prerequisites=["simple_function_integral"],
))

register_atom(Atom(
    atom_type="theorem",
    name="fubini_compute",
    content=(
        "Fubini's theorem: if f is integrable on the product space "
        "X x Y, then the double integral equals the iterated integrals: "
        "integral(f, X x Y) = integral_X(integral_Y(f(x,y) dy) dx) = "
        "integral_Y(integral_X(f(x,y) dx) dy). This justifies "
        "computing double integrals by iterated single integrals."
    ),
    example=(
        "f(x,y) = xy on [0,1] x [0,2]. "
        "integral = integral_0^1 (integral_0^2 xy dy) dx "
        "= integral_0^1 x[y^2/2]_0^2 dx = integral_0^1 2x dx "
        "= [x^2]_0^1 = 1."
    ),
    tier=7,
    domain="measure_theory",
    source="Wikipedia contributors, 'Fubini's theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fubini%27s_theorem",
    prerequisites=["simple_function_integral"],
))

register_atom(Atom(
    atom_type="definition",
    name="borel_set",
    content=(
        "A Borel set is any set that can be formed from open sets "
        "through countable unions, countable intersections, and "
        "complements. The collection of all Borel sets forms the Borel "
        "sigma-algebra B(R). Every open set, closed set, G-delta set, "
        "and F-sigma set is a Borel set."
    ),
    example=(
        "Open intervals (a,b) are Borel. Closed intervals [a,b] are "
        "Borel (complement of open). Singletons {a} = "
        "intersection([a-1/n, a+1/n], n=1..inf) are Borel (G-delta). "
        "The rationals Q = union({q}, q in Q) are Borel (countable "
        "union of singletons)."
    ),
    tier=6,
    domain="measure_theory",
    source="Wikipedia contributors, 'Borel set', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Borel_set",
    prerequisites=["sigma_algebra"],
))


# ---------------------------------------------------------------------------
# Complex Analysis (tier 6-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="cauchy_riemann",
    content=(
        "The Cauchy-Riemann equations are necessary conditions for a "
        "complex function f(z) = u(x,y) + iv(x,y) to be holomorphic "
        "(complex differentiable). They state: du/dx = dv/dy and "
        "du/dy = -dv/dx. If the partial derivatives exist and are "
        "continuous, these conditions are also sufficient."
    ),
    example=(
        "f(z) = z^2 = (x+iy)^2 = (x^2-y^2) + i(2xy). "
        "u = x^2-y^2, v = 2xy. du/dx = 2x = dv/dy = 2x. "
        "du/dy = -2y = -dv/dx = -(2y). Both satisfied, so f is "
        "holomorphic everywhere."
    ),
    tier=6,
    domain="complex_analysis",
    source="Wikipedia contributors, 'Cauchy-Riemann equations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cauchy%E2%80%93Riemann_equations",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="theorem",
    name="complex_power_series",
    content=(
        "A complex power series sum(a_n * (z - z_0)^n, n=0..inf) "
        "converges absolutely inside a disc |z - z_0| < R, where R "
        "is the radius of convergence given by the Cauchy-Hadamard "
        "formula: 1/R = lim sup |a_n|^{1/n}. The series diverges "
        "for |z - z_0| > R."
    ),
    example=(
        "sum(z^n/n!, n=0..inf) = e^z. |a_n| = 1/n!, "
        "(1/n!)^{1/n} -> 0 as n -> inf. So 1/R = 0, R = inf. "
        "The series converges for all z in C."
    ),
    tier=6,
    domain="complex_analysis",
    source="Wikipedia contributors, 'Radius of convergence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Radius_of_convergence",
    prerequisites=["cauchy_riemann"],
))

register_atom(Atom(
    atom_type="theorem",
    name="residue_compute",
    content=(
        "The residue of a meromorphic function f at an isolated "
        "singularity z_0 is Res(f, z_0) = a_{-1}, the coefficient "
        "of (z-z_0)^{-1} in the Laurent series. For a simple pole: "
        "Res(f, z_0) = lim_{z->z_0} (z-z_0)*f(z). For a pole of "
        "order n: Res = (1/(n-1)!) * lim d^{n-1}/dz^{n-1} "
        "[(z-z_0)^n * f(z)]."
    ),
    example=(
        "f(z) = 1/(z^2 + 1) = 1/((z-i)(z+i)). Simple pole at z=i: "
        "Res(f, i) = lim_{z->i} (z-i)/(z^2+1) = 1/(2i) = -i/2."
    ),
    tier=6,
    domain="complex_analysis",
    source="Wikipedia contributors, 'Residue (complex analysis)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Residue_(complex_analysis)",
    prerequisites=["laurent_series"],
))

register_atom(Atom(
    atom_type="theorem",
    name="contour_integral",
    content=(
        "The Cauchy Residue Theorem: if f is meromorphic inside and on "
        "a simple closed contour C, then the contour integral "
        "oint_C f(z) dz = 2*pi*i * sum(Res(f, z_k)) where the sum "
        "is over all poles z_k enclosed by C. This reduces contour "
        "integration to residue computation."
    ),
    example=(
        "integral of 1/(z^2+1) around |z|=2. Poles at z=i, z=-i, "
        "both inside |z|=2. Res(f,i) = 1/(2i), Res(f,-i) = -1/(2i). "
        "Sum = 0. Integral = 2*pi*i * 0 = 0."
    ),
    tier=7,
    domain="complex_analysis",
    source="Wikipedia contributors, 'Residue theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Residue_theorem",
    prerequisites=["residue_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="analytic_check",
    content=(
        "A complex function f is analytic (holomorphic) at z_0 if it "
        "is complex differentiable in a neighborhood of z_0. "
        "Equivalently, f satisfies the Cauchy-Riemann equations with "
        "continuous partial derivatives. An entire function is analytic "
        "on all of C. f(z) = |z|^2 = z*conj(z) is not analytic "
        "because it fails Cauchy-Riemann."
    ),
    example=(
        "f(z) = (3+2i)z. u = 3x-2y, v = 2x+3y. "
        "du/dx = 3 = dv/dy = 3. du/dy = -2 = -dv/dx = -2. "
        "Cauchy-Riemann satisfied, so f is analytic (entire)."
    ),
    tier=6,
    domain="complex_analysis",
    source="Wikipedia contributors, 'Analytic function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Analytic_function",
    prerequisites=["cauchy_riemann"],
))

register_atom(Atom(
    atom_type="definition",
    name="mobius_transform",
    content=(
        "A Mobius transformation (linear fractional transformation) is "
        "a function f(z) = (az+b)/(cz+d) where a,b,c,d are complex "
        "constants with ad-bc != 0. Mobius transformations map circles "
        "and lines to circles and lines, are conformal (angle-preserving), "
        "and form a group under composition."
    ),
    example=(
        "f(z) = (z-1)/(z+1). a=1,b=-1,c=1,d=1. ad-bc = 1-(-1) = 2 != 0. "
        "f(0) = -1, f(1) = 0, f(-1) = undefined (pole), "
        "f(i) = (i-1)/(i+1) = ((i-1)((-i+1))/((i+1)(-i+1)) = "
        "((-i^2+i-i+1)/(1+1)) = (2)/(2) ... f(i) = -i."
    ),
    tier=6,
    domain="complex_analysis",
    source="Wikipedia contributors, 'Mobius transformation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/M%C3%B6bius_transformation",
    prerequisites=["analytic_check"],
))

register_atom(Atom(
    atom_type="definition",
    name="laurent_series",
    content=(
        "A Laurent series is a generalization of the Taylor series that "
        "includes negative powers: f(z) = sum(a_n * (z-z_0)^n, "
        "n=-inf..inf). It converges in an annulus r < |z-z_0| < R. "
        "The principal part (negative powers) characterizes the "
        "singularity: if it is finite, z_0 is a pole; if infinite, "
        "z_0 is an essential singularity."
    ),
    example=(
        "f(z) = e^{1/z} = sum(1/(n! * z^n), n=0..inf) "
        "= 1 + 1/z + 1/(2!z^2) + ... Laurent series about z=0 "
        "has infinitely many negative powers, so z=0 is an essential "
        "singularity."
    ),
    tier=7,
    domain="complex_analysis",
    source="Wikipedia contributors, 'Laurent series', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Laurent_series",
    prerequisites=["complex_power_series"],
))

register_atom(Atom(
    atom_type="definition",
    name="poles_classify",
    content=(
        "An isolated singularity z_0 of f is classified as: "
        "(1) removable if lim_{z->z_0} (z-z_0)*f(z) = 0 "
        "(no negative Laurent terms); "
        "(2) a pole of order n if (z-z_0)^n * f(z) has a removable "
        "singularity at z_0 and n is the smallest such integer; "
        "(3) an essential singularity if the Laurent series has "
        "infinitely many negative terms."
    ),
    example=(
        "f(z) = sin(z)/z: z=0 is removable (lim = 1). "
        "g(z) = 1/z^3: z=0 is a pole of order 3. "
        "h(z) = e^{1/z}: z=0 is essential (infinitely many "
        "negative powers in Laurent series)."
    ),
    tier=7,
    domain="complex_analysis",
    source="Wikipedia contributors, 'Isolated singularity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Isolated_singularity",
    prerequisites=["laurent_series"],
))
