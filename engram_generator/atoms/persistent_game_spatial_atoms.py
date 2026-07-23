"""Knowledge atoms for persistent homology, game theory ext, and spatial ext."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ---------------------------------------------------------------------------
# Persistent Homology (tiers 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="simplicial_complex",
    content=(
        "A simplicial complex is a set of simplices (vertices, edges, "
        "triangles, tetrahedra, ...) closed under taking faces. A k-simplex "
        "is the convex hull of k+1 affinely independent points. The "
        "complex must satisfy: every face of a simplex is in the complex, "
        "and the intersection of two simplices is a face of each."
    ),
    example=(
        "Vertices {0,1,2,3}, edges {01,02,12,23}, triangle {012}. "
        "This is a valid complex: all faces of triangle {012} (edges "
        "{01,02,12} and vertices {0,1,2}) are present."
    ),
    tier=5,
    domain="persistent_homology",
    source="Wikipedia contributors, 'Simplicial complex', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Simplicial_complex",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="boundary_operator",
    content=(
        "The boundary operator d_k maps k-chains to (k-1)-chains: "
        "d_k([v0,...,vk]) = sum_{i=0}^{k} (-1)^i [v0,...,v_{i-1},v_{i+1},...,vk]. "
        "The key property: d_{k-1} . d_k = 0 (boundary of a boundary is zero). "
        "This makes the chain groups into a chain complex."
    ),
    example=(
        "d_1([0,1]) = [1] - [0]. d_2([0,1,2]) = [1,2] - [0,2] + [0,1]. "
        "d_1(d_2([0,1,2])) = (2-1) - (2-0) + (1-0) = 0."
    ),
    tier=5,
    domain="persistent_homology",
    source="Wikipedia contributors, 'Chain complex', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chain_complex",
    prerequisites=["simplicial_complex"],
))

register_atom(Atom(
    atom_type="formula",
    name="betti_from_complex",
    content=(
        "The k-th Betti number beta_k = dim(ker(d_k)) - dim(im(d_{k+1})) "
        "= dim(H_k), where H_k is the k-th homology group. beta_0 counts "
        "connected components, beta_1 counts independent loops, beta_2 "
        "counts enclosed voids. Computed via Smith normal form or rank."
    ),
    example=(
        "Triangle boundary (no fill): d_1 is 3x3, rank=2. d_2 is empty. "
        "beta_0 = 3 - 2 = 1 (connected), beta_1 = 3 - 2 - 0 = 1 (one loop)."
    ),
    tier=6,
    domain="persistent_homology",
    source="Wikipedia contributors, 'Betti number', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Betti_number",
    prerequisites=["boundary_operator"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="vietoris_rips",
    content=(
        "The Vietoris-Rips complex at scale epsilon includes all simplices "
        "whose vertices are pairwise within distance epsilon: "
        "VR(X, epsilon) = {sigma subset X : diam(sigma) <= epsilon}. "
        "As epsilon grows, new simplices appear, creating a filtration "
        "used in persistent homology."
    ),
    example=(
        "Points {A, B, C} with d(A,B)=1, d(B,C)=2, d(A,C)=3. "
        "epsilon=1: edge {AB}. epsilon=2: edges {AB, BC}. "
        "epsilon=3: triangle {ABC}."
    ),
    tier=5,
    domain="persistent_homology",
    source="Wikipedia contributors, 'Vietoris-Rips complex', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Vietoris%E2%80%93Rips_complex",
    prerequisites=["simplicial_complex"],
))

register_atom(Atom(
    atom_type="definition",
    name="persistence_diagram",
    content=(
        "A persistence diagram is a multiset of points (birth, death) in "
        "the plane, where each point represents a topological feature "
        "(component, loop, void) that appears at the birth scale and "
        "disappears at the death scale. Features far from the diagonal "
        "(long-lived) represent significant topological structure."
    ),
    example=(
        "Filtration with 3 points: component born at 0, merges at 1.5. "
        "Loop born at 2.0, filled at 3.0. Diagram: "
        "H0: {(0, 1.5), (0, inf)}, H1: {(2.0, 3.0)}."
    ),
    tier=6,
    domain="persistent_homology",
    source="Wikipedia contributors, 'Persistence diagram', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Persistent_homology",
    prerequisites=["vietoris_rips"],
))

register_atom(Atom(
    atom_type="formula",
    name="bottleneck_distance",
    content=(
        "The bottleneck distance between two persistence diagrams is "
        "d_B(D1, D2) = inf_{gamma} sup_{p in D1} ||p - gamma(p)||_inf, "
        "where gamma ranges over all bijections between D1 and D2 "
        "(including diagonal points). It measures the maximum displacement "
        "needed to match the two diagrams."
    ),
    example=(
        "D1 = {(0,2), (1,3)}, D2 = {(0,2.5), (1.2,3)}. "
        "Best matching: (0,2)->(0,2.5), (1,3)->(1.2,3). "
        "Costs: max(0, 0.5)=0.5, max(0.2, 0)=0.2. "
        "d_B = max(0.5, 0.2) = 0.5."
    ),
    tier=6,
    domain="persistent_homology",
    source="Wikipedia contributors, 'Bottleneck distance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bottleneck_distance",
    prerequisites=["persistence_diagram"],
))

# ---------------------------------------------------------------------------
# Game Theory Ext (tiers 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="extensive_form",
    content=(
        "An extensive-form game represents sequential decisions as a tree. "
        "Nodes are decision points, edges are actions, leaves have payoffs. "
        "Information sets group nodes indistinguishable to a player. "
        "Subgame perfect equilibrium is found by backward induction."
    ),
    example=(
        "Player 1 chooses L or R. If L, Player 2 chooses A or B. "
        "Payoffs: (L,A)=(3,2), (L,B)=(1,4), R=(2,2). "
        "Backward induction: P2 picks B (4>2), P1 gets 1. "
        "P1 picks R (2>1). SPE: (R, B)."
    ),
    tier=5,
    domain="game_theory_ext",
    source="Wikipedia contributors, 'Extensive-form game', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Extensive-form_game",
    prerequisites=["minimax"],
))

register_atom(Atom(
    atom_type="theorem",
    name="repeated_game",
    content=(
        "A repeated game plays a stage game multiple times. In an infinitely "
        "repeated game with discount factor delta, the Folk Theorem states "
        "that any feasible individually rational payoff can be sustained as "
        "a Nash equilibrium if delta is sufficiently close to 1. Strategies "
        "include tit-for-tat and grim trigger."
    ),
    example=(
        "Prisoner's dilemma repeated: mutual cooperation gives (3,3) each "
        "round. Grim trigger: cooperate until defection, then defect forever. "
        "Sustainable if delta >= (T-R)/(T-P) = (5-3)/(5-1) = 0.5."
    ),
    tier=6,
    domain="game_theory_ext",
    source="Wikipedia contributors, 'Repeated game', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Repeated_game",
    prerequisites=["nash_equilibrium"],
))

register_atom(Atom(
    atom_type="definition",
    name="bayesian_game",
    content=(
        "A Bayesian game models incomplete information: each player has a "
        "type drawn from a probability distribution, and players have beliefs "
        "about others' types. A Bayesian Nash equilibrium is a strategy "
        "profile where each type's strategy maximises expected payoff given "
        "beliefs about other types."
    ),
    example=(
        "Auction: 2 bidders, values drawn uniformly from [0,1]. "
        "BNE in first-price: bid v/2. With value 0.8, bid 0.4."
    ),
    tier=6,
    domain="game_theory_ext",
    source="Wikipedia contributors, 'Bayesian game', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bayesian_game",
    prerequisites=["nash_equilibrium"],
))

register_atom(Atom(
    atom_type="definition",
    name="correlated_equilibrium",
    content=(
        "A correlated equilibrium extends Nash equilibrium by allowing a "
        "mediator to send private signals to players. A joint distribution "
        "over action profiles is a CE if no player gains by deviating from "
        "the recommended action. Every NE is a CE, but CE can achieve "
        "higher social welfare."
    ),
    example=(
        "Game of chicken: NE are (Swerve, Straight) and (Straight, Swerve). "
        "A CE: mediator tells each player to go straight with prob 1/3 each, "
        "both swerve with prob 1/3. Expected payoff exceeds any NE."
    ),
    tier=6,
    domain="game_theory_ext",
    source="Wikipedia contributors, 'Correlated equilibrium', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Correlated_equilibrium",
    prerequisites=["nash_equilibrium"],
))

register_atom(Atom(
    atom_type="formula",
    name="shapley_value",
    content=(
        "The Shapley value fairly distributes the total payoff among players "
        "in a cooperative game. For player i: phi_i = sum over coalitions S "
        "not containing i of [|S|!(n-|S|-1)!/n!] * [v(S union {i}) - v(S)], "
        "where v is the characteristic function."
    ),
    example=(
        "3 players, v({1})=0, v({2})=0, v({3})=0, v({1,2})=6, v({1,3})=8, "
        "v({2,3})=7, v({1,2,3})=10. phi_1 = (0+0+4+3)/3!/... "
        "Working out: phi_1=3.5, phi_2=2.83, phi_3=3.67."
    ),
    tier=5,
    domain="game_theory_ext",
    source="Wikipedia contributors, 'Shapley value', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shapley_value",
    prerequisites=["permutation"],
))

register_atom(Atom(
    atom_type="definition",
    name="evolutionary_stable",
    content=(
        "An Evolutionarily Stable Strategy (ESS) is a strategy that, if "
        "adopted by a population, cannot be invaded by any alternative "
        "strategy. Strategy s* is ESS if for all mutant strategies s: "
        "E(s*, s*) > E(s, s*), or E(s*, s*) = E(s, s*) and E(s*, s) > E(s, s). "
        "Introduced by Maynard Smith and Price (1973)."
    ),
    example=(
        "Hawk-Dove game: V=4, C=6. E(H,H)=(V-C)/2=-1, E(H,D)=V=4, "
        "E(D,H)=0, E(D,D)=V/2=2. Mixed ESS: p*=V/C=2/3 hawk."
    ),
    tier=6,
    domain="game_theory_ext",
    source="Wikipedia contributors, 'Evolutionarily stable strategy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Evolutionarily_stable_strategy",
    prerequisites=["nash_equilibrium"],
))

# ---------------------------------------------------------------------------
# Spatial Algorithms (tiers 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="rotation_3d",
    content=(
        "3D rotation around an axis by angle theta uses rotation matrices. "
        "Around z-axis: R_z = [[cos t, -sin t, 0], [sin t, cos t, 0], [0,0,1]]. "
        "Around x-axis: R_x = [[1,0,0],[0,cos t,-sin t],[0,sin t,cos t]]. "
        "General rotation uses Rodrigues' formula: "
        "R = I + sin(t)*K + (1-cos(t))*K^2 where K is the skew-symmetric "
        "matrix of the rotation axis."
    ),
    example=(
        "Rotate (1,0,0) by 90 degrees around z-axis: "
        "R_z * [1,0,0]^T = [cos 90, sin 90, 0] = [0, 1, 0]."
    ),
    tier=5,
    domain="spatial_ext",
    source="Wikipedia contributors, 'Rotation matrix', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rotation_matrix",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="voronoi_cell",
    content=(
        "A Voronoi diagram partitions space into cells, one per site point. "
        "Each cell contains all points closer to its site than any other. "
        "The boundary between two cells is the perpendicular bisector of "
        "the line segment connecting the sites. Computed in O(n log n) "
        "by Fortune's algorithm."
    ),
    example=(
        "Sites A=(0,0), B=(4,0), C=(2,3). Voronoi vertex at circumcentre "
        "of triangle ABC. Cell of A: region closer to A than B or C."
    ),
    tier=6,
    domain="spatial_ext",
    source="Wikipedia contributors, 'Voronoi diagram', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Voronoi_diagram",
    prerequisites=["distance_2d"],
))

register_atom(Atom(
    atom_type="definition",
    name="delaunay_check",
    content=(
        "A Delaunay triangulation has the property that no point lies "
        "inside the circumcircle of any triangle. Equivalently, the "
        "minimum angle is maximised. A triangle passes the Delaunay "
        "condition if the circumcircle of each triangle contains no "
        "other points. Dual of the Voronoi diagram."
    ),
    example=(
        "Points (0,0), (4,0), (2,3), (2,1). Check triangle (0,0),(4,0),(2,3): "
        "circumcircle centre=(2,0.833), radius=2.167. Point (2,1) is inside "
        "(dist=0.167 < 2.167), so NOT Delaunay."
    ),
    tier=6,
    domain="spatial_ext",
    source="Wikipedia contributors, 'Delaunay triangulation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Delaunay_triangulation",
    prerequisites=["voronoi_cell"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="convex_hull_2d",
    content=(
        "The convex hull is the smallest convex polygon containing all "
        "points. Graham scan: pick lowest point, sort others by polar "
        "angle, process in order keeping only left turns. Gift wrapping: "
        "start from leftmost point, always pick the most counter-clockwise "
        "next point. Both O(n log n)."
    ),
    example=(
        "Points: (0,0), (1,1), (2,0), (1,2), (0.5,0.5). "
        "Hull: (0,0) -> (2,0) -> (1,2) -> (0,0). "
        "Interior points (1,1) and (0.5,0.5) excluded."
    ),
    tier=5,
    domain="spatial_ext",
    source="Wikipedia contributors, 'Convex hull algorithms', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convex_hull_algorithms",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="formula",
    name="affine_transform",
    content=(
        "An affine transformation maps points via a linear transformation "
        "plus translation: p' = A*p + t, where A is a matrix and t is "
        "a translation vector. In homogeneous coordinates: "
        "[p'; 1] = [[A, t], [0, 1]] * [p; 1]. Includes rotation, "
        "scaling, shearing, and translation."
    ),
    example=(
        "Scale by 2 and translate by (1,3): A=[[2,0],[0,2]], t=[1,3]. "
        "Point (1,1): p' = [[2,0],[0,2]]*[1,1] + [1,3] = [2,2]+[1,3] = [3,5]."
    ),
    tier=5,
    domain="spatial_ext",
    source="Wikipedia contributors, 'Affine transformation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Affine_transformation",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="closest_pair",
    content=(
        "The closest pair problem finds the two points with minimum "
        "distance among n points. Divide-and-conquer: split points by "
        "median x-coordinate, solve each half recursively, check strip "
        "around dividing line. O(n log n) time. Brute force is O(n^2)."
    ),
    example=(
        "Points: (0,0), (3,4), (1,1), (5,2), (2,3). "
        "Brute force: d(0,0)-(1,1)=sqrt(2)=1.414, "
        "d(1,1)-(2,3)=sqrt(5)=2.236. Closest pair: (0,0) and (1,1)."
    ),
    tier=5,
    domain="spatial_ext",
    source="Wikipedia contributors, 'Closest pair of points problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Closest_pair_of_points_problem",
    prerequisites=["distance_2d"],
))
