"""Knowledge atoms for combinatorial optimisation, computer graphics,
and advanced graph theory.

Each atom stores the authoritative definition or algorithm description
sourced from Wikipedia, with a worked example for verification.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ===================================================================
# Combinatorial Optimisation (tier 4-6)
# ===================================================================

register_atom(Atom(
    atom_type="algorithm",
    name="tsp_nearest_neighbor",
    content=(
        "The nearest neighbour algorithm for the Travelling Salesman "
        "Problem starts at a given city and repeatedly visits the nearest "
        "unvisited city until all cities have been visited, then returns "
        "to the starting city. It is a greedy heuristic that runs in "
        "O(n^2) time but does not guarantee an optimal solution. The "
        "approximation ratio can be as bad as O(log n) in the worst case."
    ),
    example=(
        "Cities at (0,0),(3,0),(3,4),(0,4). Start at (0,0): "
        "nearest is (3,0) d=3, then (3,4) d=4, then (0,4) d=3, "
        "return to (0,0) d=4. Tour length = 3+4+3+4 = 14."
    ),
    tier=5,
    domain="combinatorial_optimisation",
    source="Wikipedia contributors, 'Nearest neighbour algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="assignment_problem",
    content=(
        "The assignment problem seeks a minimum-cost perfect matching in "
        "a bipartite graph. Given an n x n cost matrix C, find a "
        "permutation sigma that minimises sum(C[i][sigma(i)]). The "
        "Hungarian algorithm solves this in O(n^3) time. The problem is "
        "equivalent to finding a minimum-weight perfect matching."
    ),
    example=(
        "Cost matrix [[9,2,7],[6,4,3],[5,8,1]]. "
        "Optimal assignment: 1->2(2), 2->3(3), 3->1(5). Total cost = 10."
    ),
    tier=6,
    domain="combinatorial_optimisation",
    source="Wikipedia contributors, 'Assignment problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Assignment_problem",
    prerequisites=["matching_bipartite"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="matching_bipartite",
    content=(
        "A maximum matching in a bipartite graph is a largest set of "
        "edges with no shared vertices. The Hopcroft-Karp algorithm "
        "finds it in O(E*sqrt(V)) time. A perfect matching exists iff "
        "Hall's condition is satisfied: for every subset S of one part, "
        "|N(S)| >= |S|."
    ),
    example=(
        "Bipartite graph: L={1,2,3}, R={a,b,c}, edges: "
        "1-a, 1-b, 2-b, 2-c, 3-c. Maximum matching: {1-a, 2-b, 3-c}, "
        "size 3 (perfect matching)."
    ),
    tier=5,
    domain="combinatorial_optimisation",
    source="Wikipedia contributors, 'Matching (graph theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Matching_(graph_theory)",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="job_scheduling",
    content=(
        "The job scheduling problem assigns jobs to machines to minimise "
        "makespan (total completion time). For a single machine with "
        "weighted completion times, the optimal order is Shortest "
        "Processing Time (SPT) for unweighted, or Smith's rule "
        "(sort by w_i/p_i descending) for weighted. For parallel "
        "machines, the Longest Processing Time (LPT) heuristic gives "
        "a 4/3 approximation."
    ),
    example=(
        "Jobs with processing times [3,1,4,2], single machine SPT: "
        "order [1,2,3,4] -> completions [1,3,6,10], "
        "total weighted completion = 1+3+6+10 = 20."
    ),
    tier=5,
    domain="combinatorial_optimisation",
    source="Wikipedia contributors, 'Job-shop scheduling', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Job-shop_scheduling",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="knapsack_fractional",
    content=(
        "The fractional knapsack problem allows items to be broken into "
        "fractions. The greedy algorithm sorts items by value/weight "
        "ratio in descending order and takes as much of each item as "
        "possible until the capacity is reached. This gives an optimal "
        "solution in O(n log n) time, unlike the 0/1 knapsack which "
        "is NP-hard."
    ),
    example=(
        "Items: (value=60,weight=10), (value=100,weight=20), "
        "(value=120,weight=30). Capacity=50. Ratios: 6, 5, 4. "
        "Take all of item1 (60,10), all of item2 (100,20), "
        "2/3 of item3 (80,20). Total value = 240, weight = 50."
    ),
    tier=4,
    domain="combinatorial_optimisation",
    source="Wikipedia contributors, 'Continuous knapsack problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Continuous_knapsack_problem",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="set_cover_greedy",
    content=(
        "The set cover problem seeks a minimum number of sets from a "
        "collection whose union equals the universe. The greedy "
        "algorithm repeatedly selects the set covering the most "
        "uncovered elements. It achieves an approximation ratio of "
        "H(n) = ln(n) + 1, which is the best possible unless P=NP."
    ),
    example=(
        "Universe U={1,2,3,4,5}. Sets: S1={1,2,3}, S2={2,4}, "
        "S3={3,4,5}, S4={5}. Greedy: pick S1 (covers 3), "
        "pick S3 (covers 4,5). Cover = {S1, S3}, size 2."
    ),
    tier=5,
    domain="combinatorial_optimisation",
    source="Wikipedia contributors, 'Set cover problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Set_cover_problem",
    prerequisites=["set_operations"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="bin_packing",
    content=(
        "The bin packing problem asks for the minimum number of bins of "
        "capacity C needed to pack items of given sizes. The First Fit "
        "Decreasing (FFD) heuristic sorts items in decreasing order and "
        "places each item in the first bin that has room. FFD uses at "
        "most 11/9 * OPT + 6/9 bins."
    ),
    example=(
        "Items [7,5,5,4,4,3,3,2], bin capacity 10. FFD: "
        "Bin1: 7+3=10, Bin2: 5+5=10, Bin3: 4+4+2=10, Bin4: 3. "
        "4 bins used."
    ),
    tier=5,
    domain="combinatorial_optimisation",
    source="Wikipedia contributors, 'Bin packing problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bin_packing_problem",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="integer_programming",
    content=(
        "Integer linear programming (ILP) optimises a linear objective "
        "function subject to linear constraints with the additional "
        "requirement that some or all variables must be integers. It is "
        "NP-hard in general. The LP relaxation drops the integrality "
        "constraint; branch-and-bound explores the solution tree by "
        "branching on fractional variables and bounding with LP relaxation."
    ),
    example=(
        "Maximise 5x+4y subject to x+y<=5, 10x+6y<=45, x,y>=0 integer. "
        "LP relaxation gives x=3.75, y=1.25, obj=23.75. "
        "Optimal integer: x=3, y=2, obj=23."
    ),
    tier=6,
    domain="combinatorial_optimisation",
    source="Wikipedia contributors, 'Integer programming', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Integer_programming",
    prerequisites=["linear_program"],
))


# ===================================================================
# Computer Graphics (tier 5-6)
# ===================================================================

register_atom(Atom(
    atom_type="formula",
    name="matrix_transform_3d",
    content=(
        "3D transformations in computer graphics are represented as 4x4 "
        "homogeneous matrices. Translation by (tx,ty,tz) uses a matrix "
        "with the translation in the last column. Rotation, scaling, and "
        "shearing are similarly encoded. Transformations compose by "
        "matrix multiplication, applied right-to-left."
    ),
    example=(
        "Translate point (1,2,3) by (4,5,6): "
        "[1,0,0,4; 0,1,0,5; 0,0,1,6; 0,0,0,1] * [1,2,3,1]^T "
        "= [5,7,9,1]^T. Result: (5,7,9)."
    ),
    tier=5,
    domain="computer_graphics",
    source="Wikipedia contributors, 'Transformation matrix', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Transformation_matrix",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="formula",
    name="perspective_projection",
    content=(
        "Perspective projection maps 3D points to a 2D plane by dividing "
        "by the depth coordinate, simulating how the eye sees. For a "
        "camera at the origin looking along -z with focal length f: "
        "x' = f*x/z, y' = f*y/z. This creates foreshortening where "
        "distant objects appear smaller."
    ),
    example=(
        "Point (3, 4, 10), focal length f=5: "
        "x' = 5*3/10 = 1.5, y' = 5*4/10 = 2.0. "
        "Projected point: (1.5, 2.0)."
    ),
    tier=5,
    domain="computer_graphics",
    source="Wikipedia contributors, 'Perspective projection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/3D_projection#Perspective_projection",
    prerequisites=["matrix_transform_3d"],
))

register_atom(Atom(
    atom_type="formula",
    name="ray_sphere_intersect",
    content=(
        "A ray R(t) = O + t*D intersects a sphere |P - C|^2 = r^2 when "
        "the discriminant of the quadratic is non-negative. Substituting: "
        "a = D.D, b = 2*D.(O-C), c = (O-C).(O-C) - r^2. "
        "Discriminant = b^2 - 4ac. If >= 0, t = (-b +/- sqrt(disc)) / 2a."
    ),
    example=(
        "Ray origin O=(0,0,0), direction D=(0,0,1), "
        "sphere center C=(0,0,5), radius r=1. "
        "OC=(0,0,-5), a=1, b=2*(0+0-5)=-10, c=25-1=24. "
        "disc=100-96=4, t=(10+/-2)/2 -> t=4 or t=6. "
        "Nearest hit at t=4, point (0,0,4)."
    ),
    tier=5,
    domain="computer_graphics",
    source="Wikipedia contributors, 'Line-sphere intersection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection",
    prerequisites=["dot_product", "quadratic"],
))

register_atom(Atom(
    atom_type="formula",
    name="barycentric_coords",
    content=(
        "Barycentric coordinates (u, v, w) express a point P inside a "
        "triangle with vertices A, B, C as P = u*A + v*B + w*C, where "
        "u + v + w = 1 and all are non-negative. They are computed from "
        "area ratios: u = Area(PBC)/Area(ABC), v = Area(APC)/Area(ABC), "
        "w = 1 - u - v."
    ),
    example=(
        "Triangle A=(0,0), B=(4,0), C=(0,3). Point P=(1,1). "
        "Area(ABC) = 0.5*4*3 = 6. Area(PBC) = 0.5*|det| = 2.5. "
        "u = 2.5/6 = 5/12, v = 1.5/6 = 1/4, w = 1-5/12-1/4 = 1/3."
    ),
    tier=5,
    domain="computer_graphics",
    source="Wikipedia contributors, 'Barycentric coordinate system', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Barycentric_coordinate_system",
    prerequisites=["area_triangle"],
))

register_atom(Atom(
    atom_type="formula",
    name="bezier_curve",
    content=(
        "A Bezier curve of degree n is defined by n+1 control points "
        "P0..Pn: B(t) = sum(C(n,i) * (1-t)^(n-i) * t^i * Pi, i=0..n) "
        "for t in [0,1]. A cubic Bezier (n=3) uses 4 control points: "
        "B(t) = (1-t)^3*P0 + 3(1-t)^2*t*P1 + 3(1-t)*t^2*P2 + t^3*P3."
    ),
    example=(
        "Cubic Bezier with P0=(0,0), P1=(1,2), P2=(3,2), P3=(4,0). "
        "At t=0.5: B = 0.125*(0,0) + 0.375*(1,2) + 0.375*(3,2) "
        "+ 0.125*(4,0) = (0+0.375+1.125+0.5, 0+0.75+0.75+0) = (2, 1.5)."
    ),
    tier=5,
    domain="computer_graphics",
    source="Wikipedia contributors, 'Bezier curve', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/B%C3%A9zier_curve",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="formula",
    name="phong_shading",
    content=(
        "The Phong reflection model computes surface colour as a sum of "
        "ambient, diffuse, and specular components: "
        "I = k_a*I_a + k_d*(L.N)*I_d + k_s*(R.V)^alpha * I_s, "
        "where L is the light direction, N is the surface normal, "
        "R is the reflected light direction, V is the view direction, "
        "and alpha is the shininess exponent."
    ),
    example=(
        "k_a=0.1, k_d=0.7, k_s=0.2, alpha=32, I_a=I_d=I_s=1.0. "
        "L.N=0.8, R.V=0.9. "
        "I = 0.1*1 + 0.7*0.8*1 + 0.2*0.9^32*1 "
        "= 0.1 + 0.56 + 0.2*0.0424 = 0.1 + 0.56 + 0.0085 = 0.6685."
    ),
    tier=5,
    domain="computer_graphics",
    source="Wikipedia contributors, 'Phong reflection model', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Phong_reflection_model",
    prerequisites=["dot_product"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="frustum_culling",
    content=(
        "Frustum culling tests whether objects lie inside the camera's "
        "view frustum (a truncated pyramid). An axis-aligned bounding "
        "box (AABB) is tested against the 6 planes of the frustum. If "
        "the AABB is entirely outside any plane, the object is culled "
        "(not rendered). The signed distance from point P to plane "
        "(n, d) is n.P + d."
    ),
    example=(
        "AABB min=(-1,-1,5), max=(1,1,7). Near plane z=3 (normal (0,0,1), d=-3). "
        "Min z=5 > 3, so AABB is in front of near plane. "
        "Far plane z=10 (normal (0,0,-1), d=10). Max z=7 < 10, inside. "
        "Object is inside frustum (not culled)."
    ),
    tier=5,
    domain="computer_graphics",
    source="Wikipedia contributors, 'Viewing frustum', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Viewing_frustum",
    prerequisites=["dot_product"],
))

register_atom(Atom(
    atom_type="formula",
    name="quaternion_rotate",
    content=(
        "A unit quaternion q = cos(theta/2) + sin(theta/2)*(xi + yj + zk) "
        "represents a rotation by angle theta around axis (x,y,z). "
        "To rotate vector v: v' = q * v * q^(-1), where v is treated as "
        "a pure quaternion (0, v). Quaternion multiplication avoids "
        "gimbal lock and is more efficient than rotation matrices."
    ),
    example=(
        "Rotate (1,0,0) by 90 degrees around z-axis. "
        "q = cos(45) + sin(45)*k = (0.7071, 0, 0, 0.7071). "
        "v' = q*(0,1,0,0)*q_inv = (0, 0, 1, 0). Result: (0,1,0)."
    ),
    tier=6,
    domain="computer_graphics",
    source="Wikipedia contributors, 'Quaternions and spatial rotation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation",
    prerequisites=["matrix_transform_3d"],
))


# ===================================================================
# Advanced Graph Theory (tier 5-6)
# ===================================================================

register_atom(Atom(
    atom_type="algorithm",
    name="graph_isomorphism",
    content=(
        "Two graphs G and H are isomorphic if there exists a bijection "
        "f: V(G) -> V(H) such that (u,v) is an edge in G iff "
        "(f(u),f(v)) is an edge in H. Necessary conditions include "
        "equal vertex count, edge count, and degree sequence. The "
        "problem's complexity class is GI (between P and NP-complete)."
    ),
    example=(
        "G: edges {(1,2),(2,3),(3,1)}. H: edges {(a,b),(b,c),(c,a)}. "
        "Both are triangles with degree sequence [2,2,2]. "
        "Mapping f(1)=a, f(2)=b, f(3)=c preserves all edges. Isomorphic."
    ),
    tier=6,
    domain="graph_theory",
    source="Wikipedia contributors, 'Graph isomorphism', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Graph_isomorphism",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="theorem",
    name="eulerian_path",
    content=(
        "An Eulerian path visits every edge exactly once. A connected "
        "graph has an Eulerian circuit iff every vertex has even degree. "
        "It has an Eulerian path (but not circuit) iff exactly two "
        "vertices have odd degree. Hierholzer's algorithm finds the "
        "circuit/path in O(|E|) time."
    ),
    example=(
        "Graph: edges {(A,B),(A,C),(B,C),(B,D),(C,D)}. "
        "Degrees: A=2, B=3, C=3, D=2. Two odd-degree vertices (B,C). "
        "Eulerian path exists: B-A-C-B-D-C."
    ),
    tier=5,
    domain="graph_theory",
    source="Wikipedia contributors, 'Eulerian path', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Eulerian_path",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="hamiltonian_check",
    content=(
        "A Hamiltonian path visits every vertex exactly once. A "
        "Hamiltonian cycle is a Hamiltonian path that returns to the "
        "starting vertex. Determining whether a Hamiltonian path exists "
        "is NP-complete. Sufficient conditions include Dirac's theorem: "
        "if every vertex has degree >= n/2, a Hamiltonian cycle exists."
    ),
    example=(
        "K4 (complete graph on 4 vertices): every vertex has degree 3 "
        ">= 4/2 = 2. By Dirac's theorem, Hamiltonian cycle exists. "
        "One cycle: 1-2-3-4-1."
    ),
    tier=6,
    domain="graph_theory",
    source="Wikipedia contributors, 'Hamiltonian path', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hamiltonian_path",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="definition",
    name="graph_diameter",
    content=(
        "The diameter of a graph is the maximum shortest path distance "
        "between any pair of vertices: diam(G) = max(d(u,v)) for all "
        "u, v in V. It can be computed by running BFS/Dijkstra from "
        "every vertex. For unweighted graphs this takes O(V*(V+E)) time."
    ),
    example=(
        "Path graph P4: 1-2-3-4. Shortest paths: d(1,4)=3, d(1,3)=2, "
        "d(2,4)=2. Maximum is d(1,4)=3. Diameter = 3."
    ),
    tier=5,
    domain="graph_theory",
    source="Wikipedia contributors, 'Distance (graph theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Distance_(graph_theory)",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="definition",
    name="vertex_cover",
    content=(
        "A vertex cover of a graph is a set S of vertices such that "
        "every edge has at least one endpoint in S. The minimum vertex "
        "cover problem is NP-hard. A 2-approximation: find a maximal "
        "matching M, return both endpoints of every edge in M. By "
        "Konig's theorem, in bipartite graphs the minimum vertex cover "
        "equals the maximum matching."
    ),
    example=(
        "Graph: edges {(1,2),(2,3),(3,4)}. Maximal matching: {(1,2),(3,4)}. "
        "2-approx vertex cover: {1,2,3,4} (size 4). Optimal: {2,3} (size 2)."
    ),
    tier=6,
    domain="graph_theory",
    source="Wikipedia contributors, 'Vertex cover', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Vertex_cover",
    prerequisites=["matching_bipartite"],
))

register_atom(Atom(
    atom_type="definition",
    name="independent_set",
    content=(
        "An independent set in a graph is a set of vertices with no "
        "edges between them. The maximum independent set problem is "
        "NP-hard. The complement of a minimum vertex cover is a "
        "maximum independent set: alpha(G) + beta(G) = |V|, where "
        "alpha is the independence number and beta is the vertex cover "
        "number."
    ),
    example=(
        "Graph: edges {(1,2),(2,3),(3,4),(4,1)}. (A 4-cycle.) "
        "Maximum independent set: {1,3} or {2,4}, size 2. "
        "Minimum vertex cover: {2,4} or {1,3}, size 2. "
        "alpha + beta = 2 + 2 = 4 = |V|."
    ),
    tier=6,
    domain="graph_theory",
    source="Wikipedia contributors, 'Independent set (graph theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Independent_set_(graph_theory)",
    prerequisites=["vertex_cover"],
))

register_atom(Atom(
    atom_type="theorem",
    name="network_flow_mincut",
    content=(
        "The max-flow min-cut theorem states that in a flow network, "
        "the maximum flow from source to sink equals the minimum "
        "capacity of a cut separating source and sink. A cut is a "
        "partition (S, T) of vertices with source in S and sink in T. "
        "The Ford-Fulkerson method finds max flow by augmenting along "
        "paths in the residual graph."
    ),
    example=(
        "Network: s->a(cap 10), s->b(cap 5), a->b(cap 15), "
        "a->t(cap 10), b->t(cap 10). Max flow = 15. "
        "Min cut: {s} vs {a,b,t}, capacity = 10+5 = 15."
    ),
    tier=6,
    domain="graph_theory",
    source="Wikipedia contributors, 'Max-flow min-cut theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Max-flow_min-cut_theorem",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="topological_ordering",
    content=(
        "A topological ordering of a directed acyclic graph (DAG) is a "
        "linear ordering of vertices such that for every edge (u,v), u "
        "appears before v. Kahn's algorithm repeatedly removes vertices "
        "with no incoming edges. A graph has a topological ordering iff "
        "it is a DAG."
    ),
    example=(
        "DAG: edges {(A,B),(A,C),(B,D),(C,D)}. "
        "Kahn's: start with A (in-degree 0). Remove A, decrement B,C. "
        "B and C have in-degree 0. Take B, then C, then D. "
        "Ordering: A, B, C, D."
    ),
    tier=6,
    domain="graph_theory",
    source="Wikipedia contributors, 'Topological sorting', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Topological_sorting",
    prerequisites=["topo_sort"],
))
