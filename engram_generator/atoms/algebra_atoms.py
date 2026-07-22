"""Knowledge atoms for linear algebra and abstract algebra.

Covers null space, column space, rank-nullity, change of basis,
Gram-Schmidt, Jordan form, matrix exponential, SVD, Markov chains,
group axioms, subgroups, cosets, quotient groups, rings, and fields.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Linear algebra (tiers 4-6)
# =========================================================================

register_atom(Atom(
    atom_type="definition",
    name="cross_product_triple",
    content=(
        "The scalar triple product of three vectors a, b, c is defined as "
        "a . (b x c) and equals the determinant of the 3x3 matrix formed "
        "by placing a, b, c as rows (or columns). Geometrically it gives "
        "the signed volume of the parallelepiped spanned by the three "
        "vectors. It is zero if and only if the vectors are coplanar."
    ),
    example=(
        "Given a=(1,0,0), b=(0,1,0), c=(0,0,1): "
        "a.(b x c) = det([[1,0,0],[0,1,0],[0,0,1]]) = 1"
    ),
    tier=4,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Triple product', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Triple_product",
    prerequisites=["cross_product", "determinant"],
))

register_atom(Atom(
    atom_type="definition",
    name="null_space",
    content=(
        "The null space (or kernel) of a matrix A is the set of all "
        "vectors x such that Ax = 0. It is a subspace of R^n for an "
        "m x n matrix A. The dimension of the null space is called the "
        "nullity of A. A matrix has a trivial null space (only the zero "
        "vector) if and only if it has full column rank."
    ),
    example=(
        "Given A = [[1,2],[2,4]]: row reduce to [[1,2],[0,0]], "
        "so x2 is free. null_space = span{[-2,1]^T}, nullity = 1"
    ),
    tier=5,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Kernel (linear algebra)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Kernel_(linear_algebra)",
    prerequisites=["matrix_multiply", "gaussian_elimination"],
))

register_atom(Atom(
    atom_type="definition",
    name="column_space",
    content=(
        "The column space (or range, image) of a matrix A is the set of "
        "all vectors b such that Ax = b has a solution. It is spanned by "
        "the columns of A and equals the set of all linear combinations "
        "of the columns. The dimension of the column space is the rank "
        "of the matrix. A system Ax = b is consistent if and only if b "
        "lies in the column space of A."
    ),
    example=(
        "Given A = [[1,0],[0,1],[0,0]]: columns are e1, e2, "
        "column_space = span{(1,0,0), (0,1,0)}, rank = 2"
    ),
    tier=5,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Column space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Column_space",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="theorem",
    name="rank_nullity",
    content=(
        "The rank-nullity theorem states that for any m x n matrix A, "
        "rank(A) + nullity(A) = n, where rank(A) is the dimension of "
        "the column space and nullity(A) is the dimension of the null "
        "space. Equivalently, the number of pivot columns plus the "
        "number of free variables equals the total number of columns."
    ),
    example=(
        "Given a 3x4 matrix with rank 2: nullity = 4 - 2 = 2, "
        "so the null space is 2-dimensional"
    ),
    tier=5,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Rank-nullity theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rank%E2%80%93nullity_theorem",
    prerequisites=["null_space", "column_space"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="gram_schmidt",
    content=(
        "The Gram-Schmidt process takes a set of linearly independent "
        "vectors {v1, ..., vk} and produces an orthonormal set "
        "{u1, ..., uk} spanning the same subspace. The algorithm proceeds "
        "iteratively: u1 = v1/||v1||, then for each subsequent vector, "
        "subtract projections onto all previous orthonormal vectors and "
        "normalise: u_k = (v_k - sum proj_{u_i}(v_k)) / ||...||."
    ),
    example=(
        "Given v1=(1,1,0), v2=(1,0,1): "
        "u1 = (1,1,0)/sqrt(2). "
        "v2' = (1,0,1) - ((1,0,1).(1,1,0)/2)*(1,1,0) = (1,0,1) - (1/2,1/2,0) = (1/2,-1/2,1). "
        "u2 = (1/2,-1/2,1)/||...|| = (1,-1,2)/sqrt(6)"
    ),
    tier=5,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Gram-Schmidt process', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process",
    prerequisites=["dot_product", "norm"],
))

register_atom(Atom(
    atom_type="definition",
    name="quadratic_form",
    content=(
        "A quadratic form on R^n is a function Q(x) = x^T A x, where A "
        "is a symmetric n x n matrix. The quadratic form is positive "
        "definite if Q(x) > 0 for all nonzero x, which is equivalent to "
        "all eigenvalues of A being positive. The matrix of a quadratic "
        "form can be recovered from the form by A_ij = (1/2) d^2Q/dx_i dx_j."
    ),
    example=(
        "Given Q(x,y) = 2x^2 + 3y^2 + 2xy: "
        "A = [[2,1],[1,3]], eigenvalues = (5+sqrt(5))/2, (5-sqrt(5))/2, "
        "both positive, so Q is positive definite"
    ),
    tier=5,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Quadratic form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quadratic_form",
    prerequisites=["eigenvalue", "matrix_multiply"],
))

register_atom(Atom(
    atom_type="definition",
    name="projection_matrix",
    content=(
        "The orthogonal projection matrix onto the column space of a "
        "matrix A is P = A(A^T A)^{-1} A^T. It satisfies P^2 = P "
        "(idempotent) and P^T = P (symmetric). For a unit vector u, "
        "the projection matrix is P = uu^T. The projection of a vector "
        "b onto the column space is Pb, and the residual b - Pb is "
        "orthogonal to the column space."
    ),
    example=(
        "Given a = (1,1)^T: P = aa^T/(a^T a) = [[1,1],[1,1]]/2 = "
        "[[0.5,0.5],[0.5,0.5]]. "
        "Project b=(3,1): Pb = [[0.5,0.5],[0.5,0.5]]*(3,1) = (2,2)"
    ),
    tier=5,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Projection (linear algebra)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Projection_(linear_algebra)",
    prerequisites=["matrix_inverse", "matrix_multiply"],
))

register_atom(Atom(
    atom_type="definition",
    name="markov_steady_state",
    content=(
        "The stationary (steady-state) distribution of a Markov chain "
        "with transition matrix P is a probability vector pi such that "
        "pi P = pi and sum(pi_i) = 1. For an irreducible, aperiodic "
        "chain, the stationary distribution exists, is unique, and the "
        "chain converges to it regardless of the initial state. It can "
        "be found by solving the linear system (P^T - I) pi = 0 with "
        "the constraint sum(pi_i) = 1."
    ),
    example=(
        "Given P = [[0.7,0.3],[0.4,0.6]]: solve pi*P = pi. "
        "0.7*pi1 + 0.4*pi2 = pi1 => pi2 = pi1, and pi1+pi2=1: "
        "pi = [4/7, 3/7] = [0.5714, 0.4286]"
    ),
    tier=5,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Markov chain', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Markov_chain#Stationary_distribution_relation_to_eigenvectors_and_simplices",
    prerequisites=["eigenvalue", "matrix_multiply"],
))

register_atom(Atom(
    atom_type="definition",
    name="change_of_basis",
    content=(
        "A change of basis transforms coordinates of a vector from one "
        "basis to another. If B = {b1,...,bn} and C = {c1,...,cn} are "
        "two bases for V, the change-of-basis matrix P from B to C has "
        "columns [b1]_C, ..., [bn]_C (coordinates of each B-basis vector "
        "in the C-basis). Then [v]_C = P [v]_B. For a linear map T, the "
        "matrix representation changes as [T]_C = P^{-1} [T]_B P."
    ),
    example=(
        "Given standard basis B and new basis C = {(1,1),(1,-1)}: "
        "P = [[1,1],[1,-1]], P^{-1} = [[1/2,1/2],[1/2,-1/2]]. "
        "Vector (3,1) in B: [v]_C = P^{-1}*(3,1) = (2, 1)"
    ),
    tier=6,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Change of basis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Change_of_basis",
    prerequisites=["matrix_inverse", "matrix_multiply"],
))

register_atom(Atom(
    atom_type="definition",
    name="jordan_form",
    content=(
        "The Jordan normal form of a square matrix A is a block diagonal "
        "matrix J = P^{-1}AP, where each block is a Jordan block of the "
        "form J_k(lambda) with eigenvalue lambda on the diagonal and 1s "
        "on the superdiagonal. Every square matrix over C has a Jordan "
        "form, unique up to permutation of blocks. A matrix is "
        "diagonalisable if and only if all Jordan blocks are 1x1."
    ),
    example=(
        "Given A = [[5,4,2,1],[0,1,-1,-1],[-1,-1,3,0],[1,1,-1,2]]: "
        "eigenvalues are 1,2,4,4. If 4 has geometric multiplicity 1, "
        "Jordan form has a 2x2 block: J = diag(1, 2, [[4,1],[0,4]])"
    ),
    tier=6,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Jordan normal form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Jordan_normal_form",
    prerequisites=["eigenvalue", "null_space"],
))

register_atom(Atom(
    atom_type="formula",
    name="matrix_exponential",
    content=(
        "The matrix exponential of a square matrix A is defined as "
        "exp(A) = sum_{k=0}^{inf} A^k / k! = I + A + A^2/2! + A^3/3! + ... "
        "It converges for all square matrices. For a diagonalisable matrix "
        "A = P D P^{-1}, exp(A) = P exp(D) P^{-1} where exp(D) has "
        "exp(lambda_i) on the diagonal. The matrix exponential solves the "
        "system dx/dt = Ax with solution x(t) = exp(At) x(0)."
    ),
    example=(
        "Given A = [[0,1],[-1,0]] (rotation generator): "
        "exp(A) = [[cos(1), sin(1)],[-sin(1), cos(1)]] = "
        "[[0.5403, 0.8415],[-0.8415, 0.5403]]"
    ),
    tier=6,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Matrix exponential', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Matrix_exponential",
    prerequisites=["eigenvalue", "matrix_multiply"],
))

register_atom(Atom(
    atom_type="theorem",
    name="singular_value_decomp",
    content=(
        "The singular value decomposition (SVD) of an m x n matrix A is "
        "A = U S V^T, where U is m x m unitary, S is m x n diagonal with "
        "non-negative real entries (singular values) in decreasing order, "
        "and V is n x n unitary. The singular values are the square roots "
        "of the eigenvalues of A^T A. The rank of A equals the number of "
        "nonzero singular values. SVD exists for every matrix."
    ),
    example=(
        "Given A = [[3,2],[2,3]]: A^T A = [[13,12],[12,13]], "
        "eigenvalues 25 and 1, singular values 5 and 1. "
        "SVD: U = [[1,1],[1,-1]]/sqrt(2), S = diag(5,1), "
        "V = [[1,1],[1,-1]]/sqrt(2)"
    ),
    tier=6,
    domain="linear_algebra",
    source="Wikipedia contributors, 'Singular value decomposition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Singular_value_decomposition",
    prerequisites=["eigenvalue", "matrix_multiply"],
))


# =========================================================================
# Abstract algebra (tiers 5-6)
# =========================================================================

register_atom(Atom(
    atom_type="definition",
    name="group_axiom_check",
    content=(
        "A group (G, *) is a set G with a binary operation * satisfying "
        "four axioms: (1) Closure: a*b is in G for all a,b in G. "
        "(2) Associativity: (a*b)*c = a*(b*c). (3) Identity: there "
        "exists e in G such that e*a = a*e = a. (4) Inverse: for each "
        "a in G, there exists a^{-1} such that a*a^{-1} = a^{-1}*a = e."
    ),
    example=(
        "Given G = {0,1,2,3} under addition mod 4: "
        "closure: (2+3) mod 4 = 1 in G. "
        "associativity: ((1+2)+3) mod 4 = (1+(2+3)) mod 4 = 2. "
        "identity: 0. inverse of 3: 1 (since 3+1=0 mod 4). All axioms hold."
    ),
    tier=5,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Group (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Group_(mathematics)",
    prerequisites=["modular"],
))

register_atom(Atom(
    atom_type="theorem",
    name="subgroup_test",
    content=(
        "A nonempty subset H of a group G is a subgroup if and only if "
        "for all a, b in H, the element ab^{-1} is also in H (the "
        "one-step subgroup test). Equivalently, H is a subgroup if it "
        "is closed under the group operation and taking inverses. Every "
        "group has at least two subgroups: the trivial group {e} and G "
        "itself."
    ),
    example=(
        "In Z_6 = {0,1,2,3,4,5} under addition mod 6: "
        "H = {0,2,4}. Check: 2+4=0, 4+2=0, 2+2=4, 4+4=2, all in H. "
        "Inverses: inv(2)=4, inv(4)=2, inv(0)=0, all in H. "
        "H is a subgroup of order 3."
    ),
    tier=5,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Subgroup', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Subgroup",
    prerequisites=["group_axiom_check"],
))

register_atom(Atom(
    atom_type="definition",
    name="coset_enumerate",
    content=(
        "For a subgroup H of a group G and an element g in G, the left "
        "coset of H by g is gH = {gh : h in H}. The right coset is "
        "Hg = {hg : h in H}. Cosets partition G into disjoint subsets "
        "of equal size |H|. The number of distinct cosets [G:H] = |G|/|H| "
        "is called the index of H in G."
    ),
    example=(
        "In Z_6, H = {0,3}. Cosets: "
        "0+H = {0,3}, 1+H = {1,4}, 2+H = {2,5}. "
        "Three cosets, index [Z_6:H] = 6/2 = 3."
    ),
    tier=5,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Coset', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coset",
    prerequisites=["subgroup_test"],
))

register_atom(Atom(
    atom_type="theorem",
    name="lagrange_verify",
    content=(
        "Lagrange's theorem states that for a finite group G and a "
        "subgroup H, the order of H divides the order of G: "
        "|H| divides |G|. Equivalently, |G| = [G:H] * |H|, where "
        "[G:H] is the index. As a corollary, the order of any element "
        "divides the order of the group."
    ),
    example=(
        "G = S_3 (symmetric group, |G|=6). Subgroup H = {e, (12)} "
        "has |H|=2. Check: 2 divides 6. "
        "Index [S_3:H] = 6/2 = 3 cosets."
    ),
    tier=5,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Lagrange\\'s theorem (group theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lagrange%27s_theorem_(group_theory)",
    prerequisites=["coset_enumerate", "subgroup_test"],
))

register_atom(Atom(
    atom_type="definition",
    name="symmetric_group",
    content=(
        "The symmetric group S_n is the group of all permutations of "
        "the set {1, 2, ..., n} under composition. It has order n!. "
        "Every permutation can be written as a product of disjoint "
        "cycles. The sign (or parity) of a permutation is +1 for even "
        "permutations and -1 for odd permutations. The alternating "
        "group A_n consists of all even permutations and has order n!/2."
    ),
    example=(
        "S_3 has 3! = 6 elements: e, (12), (13), (23), (123), (132). "
        "Composition: (12)(123) = (23). Sign of (123) = +1 (even, "
        "since (123) = (12)(13), a product of 2 transpositions)."
    ),
    tier=5,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Symmetric group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Symmetric_group",
    prerequisites=["group_axiom_check"],
))

register_atom(Atom(
    atom_type="definition",
    name="cyclic_group_gen",
    content=(
        "A cyclic group is a group generated by a single element g: "
        "G = <g> = {g^k : k in Z}. Every cyclic group is abelian. "
        "A finite cyclic group of order n is isomorphic to Z_n "
        "(integers mod n under addition). The generators of Z_n are "
        "the elements coprime to n. The number of generators is "
        "phi(n), where phi is Euler's totient function."
    ),
    example=(
        "Z_8 = <1>: generators are {1,3,5,7} (coprime to 8), "
        "phi(8) = 4. The element 3 generates: "
        "3, 6, 1, 4, 7, 2, 5, 0 (all of Z_8)."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Cyclic group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cyclic_group",
    prerequisites=["group_axiom_check", "totient"],
))

register_atom(Atom(
    atom_type="definition",
    name="normal_subgroup",
    content=(
        "A subgroup N of G is normal (written N <| G) if gNg^{-1} = N "
        "for all g in G, i.e., N is invariant under conjugation. "
        "Equivalently, left and right cosets coincide: gN = Ng for all g. "
        "Normal subgroups are exactly the kernels of group homomorphisms. "
        "Every subgroup of an abelian group is normal."
    ),
    example=(
        "In S_3, the subgroup A_3 = {e, (123), (132)} is normal: "
        "for any sigma in S_3, sigma A_3 sigma^{-1} = A_3. "
        "But H = {e, (12)} is NOT normal: (123){e,(12)}(132) = {e,(23)} != H."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Normal subgroup', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Normal_subgroup",
    prerequisites=["subgroup_test", "coset_enumerate"],
))

register_atom(Atom(
    atom_type="definition",
    name="quotient_group",
    content=(
        "For a normal subgroup N of G, the quotient group (or factor "
        "group) G/N is the set of all cosets {gN : g in G} with the "
        "operation (g1 N)(g2 N) = (g1 g2)N. This is well-defined "
        "precisely because N is normal. The order of G/N is [G:N] = "
        "|G|/|N|. The natural projection pi: G -> G/N, pi(g) = gN, "
        "is a surjective homomorphism with kernel N."
    ),
    example=(
        "G = Z_6, N = {0,3} (normal, since Z_6 is abelian). "
        "G/N = {N, 1+N, 2+N} = {{0,3}, {1,4}, {2,5}}. "
        "Operation: (1+N)+(2+N) = 3+N = N = 0+N. "
        "G/N is isomorphic to Z_3."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Quotient group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quotient_group",
    prerequisites=["normal_subgroup", "coset_enumerate"],
))

register_atom(Atom(
    atom_type="definition",
    name="kernel_compute",
    content=(
        "The kernel of a group homomorphism phi: G -> H is the set "
        "ker(phi) = {g in G : phi(g) = e_H}, where e_H is the "
        "identity of H. The kernel is always a normal subgroup of G. "
        "A homomorphism is injective (one-to-one) if and only if "
        "its kernel is trivial ({e_G}). By the first isomorphism "
        "theorem, G/ker(phi) is isomorphic to im(phi)."
    ),
    example=(
        "phi: Z -> Z_3 defined by phi(n) = n mod 3. "
        "ker(phi) = {n : n mod 3 = 0} = 3Z = {...,-3,0,3,6,...}. "
        "Z/3Z is isomorphic to Z_3."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Kernel (algebra)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Kernel_(algebra)",
    prerequisites=["normal_subgroup"],
))

register_atom(Atom(
    atom_type="definition",
    name="isomorphism_check",
    content=(
        "A group isomorphism is a bijective homomorphism phi: G -> H, "
        "meaning phi(ab) = phi(a)phi(b) for all a,b in G and phi is "
        "both injective and surjective. Two groups are isomorphic "
        "(G ~ H) if such a map exists. Isomorphic groups have the "
        "same order, the same number of elements of each order, and "
        "identical structural properties."
    ),
    example=(
        "G = Z_4 = {0,1,2,3} under +mod4, H = {1,i,-1,-i} under "
        "complex multiplication. phi(k) = i^k: phi(0)=1, phi(1)=i, "
        "phi(2)=-1, phi(3)=-i. Check: phi(2+3)=phi(1)=i, "
        "phi(2)*phi(3)=(-1)(-i)=i. Isomorphism confirmed."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Group isomorphism', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Group_isomorphism",
    prerequisites=["group_axiom_check"],
))

register_atom(Atom(
    atom_type="definition",
    name="ring_ideal_check",
    content=(
        "An ideal I of a ring R is a subset that is (1) a subgroup "
        "under addition, and (2) absorbs multiplication: for all r in R "
        "and a in I, both ra and ar are in I. An ideal is proper if "
        "I != R. A maximal ideal M is a proper ideal such that no "
        "proper ideal strictly contains M. For a commutative ring, "
        "R/M is a field if and only if M is maximal."
    ),
    example=(
        "In Z, I = 6Z = {...,-6,0,6,12,...}. Check: "
        "closed under addition: 6+(-6)=0 in I. "
        "Absorbs: 5*6=30 in I. "
        "Z/6Z = Z_6, which is not a field (6Z is not maximal; "
        "2Z and 3Z are maximal ideals of Z)."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Ideal (ring theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ideal_(ring_theory)",
    prerequisites=["group_axiom_check", "modular"],
))

register_atom(Atom(
    atom_type="definition",
    name="field_extension",
    content=(
        "A field extension L/K is a pair of fields K contained in L, "
        "where L is viewed as a vector space over K. The degree [L:K] "
        "is the dimension of L as a K-vector space. An extension is "
        "algebraic if every element of L is a root of some polynomial "
        "in K[x]. A simple extension K(alpha) is generated by "
        "adjoining a single element alpha to K."
    ),
    example=(
        "Q(sqrt(2))/Q: Q(sqrt(2)) = {a + b*sqrt(2) : a,b in Q}. "
        "Basis: {1, sqrt(2)}, degree [Q(sqrt(2)):Q] = 2. "
        "sqrt(2) is algebraic over Q (root of x^2 - 2 = 0)."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Field extension', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Field_extension",
    prerequisites=["polynomial_ring"],
))
