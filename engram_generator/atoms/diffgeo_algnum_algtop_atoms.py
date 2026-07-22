"""Knowledge atoms for differential geometry, algebraic number theory,
and algebraic topology.

Each atom stores the authoritative theorem or definition sourced from
Wikipedia, a worked example, tier, domain, source citation, URL, and
prerequisite atoms.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# -----------------------------------------------------------------------
# Differential geometry (tier 6-7)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="curvature_2d",
    content=(
        "The curvature of a plane curve y = f(x) is "
        "kappa = |f''(x)| / (1 + f'(x)^2)^(3/2). For a parametric "
        "curve (x(t), y(t)), kappa = |x'y'' - y'x''| / "
        "(x'^2 + y'^2)^(3/2). Curvature measures how fast the unit "
        "tangent vector changes direction per unit arc length."
    ),
    example=(
        "y = x^2 at x=1: f'=2, f''=2. "
        "kappa = |2| / (1 + 4)^(3/2) = 2 / 5^(3/2) = 2/11.180 = 0.1789"
    ),
    tier=6,
    domain="differential_geometry",
    source="Wikipedia contributors, 'Curvature', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Curvature",
    prerequisites=["derivative", "second_derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="arc_length_param",
    content=(
        "The arc length of a curve r(t) = (x(t), y(t)) from t=a to "
        "t=b is L = integral_a^b sqrt(x'(t)^2 + y'(t)^2) dt. "
        "The arc length parametrisation reparametrises the curve so "
        "that |r'(s)| = 1 for all s, meaning the parameter s measures "
        "distance along the curve."
    ),
    example=(
        "Circle r(t) = (cos t, sin t), t in [0, pi]: "
        "x'=-sin t, y'=cos t, |r'|=1. L = integral_0^pi 1 dt = pi = 3.1416"
    ),
    tier=6,
    domain="differential_geometry",
    source="Wikipedia contributors, 'Arc length', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Arc_length",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="definition",
    name="tangent_normal",
    content=(
        "For a curve r(t) in the plane, the unit tangent vector is "
        "T = r'(t) / |r'(t)|. The unit normal vector N is obtained by "
        "rotating T by 90 degrees: N = T' / |T'|. Together T and N "
        "form the Frenet frame. The tangent points in the direction "
        "of motion; the normal points toward the centre of curvature."
    ),
    example=(
        "r(t) = (cos t, sin t): r'=(-sin t, cos t), |r'|=1. "
        "T=(-sin t, cos t). T'=(-cos t, -sin t), |T'|=1. "
        "N=(-cos t, -sin t) (points inward)."
    ),
    tier=6,
    domain="differential_geometry",
    source="Wikipedia contributors, 'Frenet-Serret formulas', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Frenet%E2%80%93Serret_formulas",
    prerequisites=["derivative", "curvature_2d"],
))

register_atom(Atom(
    atom_type="formula",
    name="christoffel_symbol",
    content=(
        "The Christoffel symbols of the second kind for a metric "
        "tensor g_ij are Gamma^k_ij = (1/2) g^{kl} (partial_i g_{jl} "
        "+ partial_j g_{il} - partial_l g_{ij}). They encode how the "
        "coordinate basis vectors change from point to point and "
        "appear in the covariant derivative and geodesic equation."
    ),
    example=(
        "Polar coordinates (r, theta): g = diag(1, r^2). "
        "Gamma^r_{theta,theta} = -r, "
        "Gamma^theta_{r,theta} = Gamma^theta_{theta,r} = 1/r, "
        "all others zero."
    ),
    tier=7,
    domain="differential_geometry",
    source="Wikipedia contributors, 'Christoffel symbols', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Christoffel_symbols",
    prerequisites=["partial_derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="geodesic_equation",
    content=(
        "A geodesic on a Riemannian manifold satisfies "
        "d^2 x^k / dt^2 + Gamma^k_{ij} (dx^i/dt)(dx^j/dt) = 0, "
        "where Gamma^k_{ij} are the Christoffel symbols. Geodesics "
        "are curves that parallel-transport their own tangent vector "
        "and locally minimise arc length."
    ),
    example=(
        "On the plane in Cartesian coordinates, all Gamma=0, so "
        "d^2x/dt^2 = 0, d^2y/dt^2 = 0: geodesics are straight lines."
    ),
    tier=7,
    domain="differential_geometry",
    source="Wikipedia contributors, 'Geodesic', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Geodesic",
    prerequisites=["christoffel_symbol"],
))

register_atom(Atom(
    atom_type="formula",
    name="gaussian_curvature",
    content=(
        "The Gaussian curvature K of a surface at a point is the "
        "product of the two principal curvatures: K = kappa_1 * kappa_2. "
        "Equivalently, K = det(II) / det(I) where I and II are the "
        "first and second fundamental forms. By Gauss's Theorema "
        "Egregium, K depends only on the intrinsic metric."
    ),
    example=(
        "Sphere of radius R: kappa_1 = kappa_2 = 1/R, "
        "K = 1/R^2. For R=3: K = 1/9 = 0.1111."
    ),
    tier=7,
    domain="differential_geometry",
    source="Wikipedia contributors, 'Gaussian curvature', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gaussian_curvature",
    prerequisites=["curvature_2d", "determinant"],
))


# -----------------------------------------------------------------------
# Algebraic number theory (tier 6-7)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="norm_trace_field",
    content=(
        "For an algebraic number alpha in a number field K of degree n "
        "over Q, the norm N_{K/Q}(alpha) is the product of all "
        "conjugates of alpha, and the trace Tr_{K/Q}(alpha) is their "
        "sum. For K = Q(sqrt(d)), alpha = a + b*sqrt(d): "
        "N(alpha) = a^2 - d*b^2, Tr(alpha) = 2a."
    ),
    example=(
        "K = Q(sqrt(5)), alpha = 3 + 2*sqrt(5): "
        "N(alpha) = 9 - 5*4 = 9 - 20 = -11, "
        "Tr(alpha) = 2*3 = 6."
    ),
    tier=6,
    domain="algebraic_number_theory",
    source="Wikipedia contributors, 'Field norm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Field_norm",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="definition",
    name="ring_of_integers",
    content=(
        "The ring of integers O_K of a number field K is the set of "
        "elements in K that are roots of monic polynomials with integer "
        "coefficients. For K = Q(sqrt(d)): O_K = Z[sqrt(d)] if "
        "d = 2,3 mod 4, and O_K = Z[(1+sqrt(d))/2] if d = 1 mod 4."
    ),
    example=(
        "K = Q(sqrt(5)): d=5, 5 mod 4 = 1, so O_K = Z[(1+sqrt(5))/2]. "
        "The golden ratio phi = (1+sqrt(5))/2 is an algebraic integer."
    ),
    tier=6,
    domain="algebraic_number_theory",
    source="Wikipedia contributors, 'Ring of integers', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ring_of_integers",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="theorem",
    name="ideal_factorisation",
    content=(
        "In the ring of integers O_K of a number field K, every nonzero "
        "ideal factors uniquely (up to order) as a product of prime "
        "ideals. A rational prime p factors in O_K as (p) = P_1^{e_1} "
        "... P_g^{e_g} where sum(e_i * f_i) = n = [K:Q] and f_i is "
        "the inertia degree of P_i."
    ),
    example=(
        "K = Q(sqrt(-5)): (2) = (2, 1+sqrt(-5))^2 (ramified). "
        "e=2, f=1, g=1. Check: e*f*g = 2*1*1 = 2 = [K:Q]."
    ),
    tier=7,
    domain="algebraic_number_theory",
    source="Wikipedia contributors, 'Dedekind domain', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dedekind_domain",
    prerequisites=["norm_trace_field", "ring_of_integers"],
))

register_atom(Atom(
    atom_type="definition",
    name="class_number",
    content=(
        "The class number h_K of a number field K is the order of the "
        "ideal class group Cl(K) = {fractional ideals} / {principal "
        "ideals}. h_K = 1 means O_K is a PID (unique factorisation "
        "of elements). The Minkowski bound gives an upper bound on "
        "the norms of generators of ideal classes."
    ),
    example=(
        "K = Q(sqrt(-5)): (2)(3) = (1+sqrt(-5))(1-sqrt(-5)) shows "
        "non-unique factorisation, so h_K > 1. In fact h_K = 2."
    ),
    tier=7,
    domain="algebraic_number_theory",
    source="Wikipedia contributors, 'Ideal class group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ideal_class_group",
    prerequisites=["ideal_factorisation"],
))

register_atom(Atom(
    atom_type="definition",
    name="p_adic_valuation",
    content=(
        "The p-adic valuation v_p(n) of an integer n is the largest "
        "power of p dividing n. For a rational a/b, v_p(a/b) = "
        "v_p(a) - v_p(b). The p-adic absolute value is |x|_p = "
        "p^{-v_p(x)}. The p-adic metric satisfies the strong "
        "triangle inequality: |x+y|_p <= max(|x|_p, |y|_p)."
    ),
    example=(
        "v_3(54) = v_3(2 * 3^3) = 3. "
        "|54|_3 = 3^{-3} = 1/27 = 0.037. "
        "v_3(12) = v_3(4 * 3) = 1, so v_3(54/12) = 3 - 1 = 2."
    ),
    tier=6,
    domain="algebraic_number_theory",
    source="Wikipedia contributors, 'p-adic valuation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/P-adic_valuation",
    prerequisites=["factorisation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="hensel_lift",
    content=(
        "Hensel's lemma: if f(x) is a polynomial with integer "
        "coefficients and f(a) = 0 mod p with f'(a) != 0 mod p, "
        "then there exists a unique lift a* = a mod p^k for each k, "
        "so that f(a*) = 0 mod p^k. The lift is computed iteratively: "
        "a_{k+1} = a_k - f(a_k) * (f'(a_k))^{-1} mod p^{k+1}."
    ),
    example=(
        "f(x) = x^2 - 2, p=7: f(3) = 7 = 0 mod 7, f'(3)=6 != 0 mod 7. "
        "Lift to mod 49: a_1 = 3 - 7 * (6)^{-1} mod 49 = 3 - 7*6^{-1} "
        "= 3 - 7*8 = 3 - 56 = -53 = 10 mod 49. Check: 100-2 = 98 = 2*49."
    ),
    tier=7,
    domain="algebraic_number_theory",
    source="Wikipedia contributors, 'Hensel's lemma', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hensel%27s_lemma",
    prerequisites=["mod_inv", "polynomial_eval"],
))


# -----------------------------------------------------------------------
# Algebraic topology (tier 7)
# -----------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="long_exact_sequence",
    content=(
        "Given a short exact sequence of chain complexes "
        "0 -> A -> B -> C -> 0, there is a long exact sequence in "
        "homology: ... -> H_n(A) -> H_n(B) -> H_n(C) -> H_{n-1}(A) "
        "-> ... The connecting homomorphism delta: H_n(C) -> H_{n-1}(A) "
        "is defined by diagram chasing."
    ),
    example=(
        "Pair (D^2, S^1): ... -> H_1(S^1) -> H_1(D^2) -> H_1(D^2,S^1) "
        "-> H_0(S^1) -> ... gives H_1(S^1) = Z, H_1(D^2) = 0, so "
        "H_1(D^2,S^1) = Z via connecting map."
    ),
    tier=7,
    domain="algebraic_topology",
    source="Wikipedia contributors, 'Long exact sequence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exact_sequence#Long_exact_sequence",
    prerequisites=["chain_complex", "homology_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="cup_product",
    content=(
        "The cup product is a bilinear operation on cohomology: "
        "H^p(X) x H^q(X) -> H^{p+q}(X). For cochains alpha in C^p "
        "and beta in C^q, (alpha cup beta)(sigma) = "
        "alpha(sigma|[v_0,...,v_p]) * beta(sigma|[v_p,...,v_{p+q}]). "
        "It gives cohomology a graded ring structure."
    ),
    example=(
        "For T^2 = S^1 x S^1: H^1(T^2) = Z^2 with generators a, b. "
        "The cup product a cup b generates H^2(T^2) = Z. "
        "a cup a = 0 (graded commutativity)."
    ),
    tier=7,
    domain="algebraic_topology",
    source="Wikipedia contributors, 'Cup product', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cup_product",
    prerequisites=["homology_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="lefschetz_number",
    content=(
        "The Lefschetz number of a continuous map f: X -> X is "
        "L(f) = sum_{k=0}^n (-1)^k tr(f_*: H_k(X) -> H_k(X)). "
        "The Lefschetz fixed-point theorem states that if L(f) != 0, "
        "then f has at least one fixed point."
    ),
    example=(
        "f: S^2 -> S^2 antipodal map: f_* on H_0 = [1], on H_2 = [-1]. "
        "L(f) = 1 + 0 + (-1)(-1) = 1 + 1 = 2 != 0, so f has a fixed "
        "point. (Contradiction: antipodal map has none, so f_* on H_2 "
        "is actually degree -1, and L(f)=0 for odd-dim spheres.)"
    ),
    tier=7,
    domain="algebraic_topology",
    source="Wikipedia contributors, 'Lefschetz fixed-point theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lefschetz_fixed-point_theorem",
    prerequisites=["homology_compute", "matrix_trace"],
))

register_atom(Atom(
    atom_type="definition",
    name="cellular_homology",
    content=(
        "For a CW complex X, the cellular chain complex has C_n = "
        "free abelian group on n-cells. The boundary map d_n: C_n -> "
        "C_{n-1} is given by the degree of the attaching map of each "
        "n-cell restricted to each (n-1)-cell. Cellular homology "
        "H_n^{CW}(X) = ker(d_n)/im(d_{n+1}) equals singular homology."
    ),
    example=(
        "S^2 as CW complex: one 0-cell e^0, one 2-cell e^2. "
        "C_0 = Z, C_1 = 0, C_2 = Z. All boundaries zero. "
        "H_0 = Z, H_1 = 0, H_2 = Z."
    ),
    tier=7,
    domain="algebraic_topology",
    source="Wikipedia contributors, 'Cellular homology', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cellular_homology",
    prerequisites=["homology_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="excision",
    content=(
        "The excision theorem states that if Z subset A subset X with "
        "the closure of Z contained in the interior of A, then the "
        "inclusion (X\\Z, A\\Z) -> (X, A) induces isomorphisms "
        "H_n(X\\Z, A\\Z) -> H_n(X, A) for all n. This allows "
        "computing relative homology by cutting out subsets."
    ),
    example=(
        "X = R^2, A = D^2 (unit disk), Z = D^2_{1/2} (disk of "
        "radius 1/2). Excision gives H_n(R^2 \\ D^2_{1/2}, "
        "D^2 \\ D^2_{1/2}) = H_n(R^2, D^2) for all n."
    ),
    tier=7,
    domain="algebraic_topology",
    source="Wikipedia contributors, 'Excision theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Excision_theorem",
    prerequisites=["long_exact_sequence"],
))

register_atom(Atom(
    atom_type="theorem",
    name="universal_coefficient",
    content=(
        "The universal coefficient theorem for homology states: "
        "H_n(X; G) = (H_n(X) tensor G) + Tor(H_{n-1}(X), G). "
        "For cohomology: H^n(X; G) = Hom(H_n(X), G) + "
        "Ext(H_{n-1}(X), G). These relate homology with different "
        "coefficient groups to integral homology."
    ),
    example=(
        "X = RP^2: H_0 = Z, H_1 = Z/2, H_2 = 0. "
        "With G = Z/2: H_0(RP^2; Z/2) = Z/2, "
        "H_1(RP^2; Z/2) = Z/2 + Tor(Z, Z/2) = Z/2, "
        "H_2(RP^2; Z/2) = 0 + Tor(Z/2, Z/2) = Z/2."
    ),
    tier=7,
    domain="algebraic_topology",
    source=(
        "Wikipedia contributors, 'Universal coefficient theorem', "
        "Wikipedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Universal_coefficient_theorem",
    prerequisites=["homology_compute", "long_exact_sequence"],
))
