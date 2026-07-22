"""Knowledge atoms for ML operations, computational geometry, and open problems.

Covers neural network building blocks (ReLU, BatchNorm, convolution,
attention), computational geometry (centroids, circumcenters, convex
hulls), and famous open problems (Goldbach, twin primes, Collatz).
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Machine Learning operations (tier 4-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="relu_derivative",
    content=(
        "The Rectified Linear Unit (ReLU) activation function is "
        "f(x) = max(0, x). Its derivative is f'(x) = 1 if x > 0, "
        "f'(x) = 0 if x < 0, and undefined at x = 0 (conventionally "
        "set to 0 or 1). ReLU avoids the vanishing gradient problem "
        "of sigmoid/tanh for positive inputs."
    ),
    example="x = [-2, 0.5, 3, -1]: ReLU = [0, 0.5, 3, 0], derivative = [0, 1, 1, 0].",
    tier=4,
    domain="machine_learning",
    source="Wikipedia contributors, 'Rectifier (neural networks)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rectifier_(neural_networks)",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="batch_norm_forward",
    content=(
        "Batch normalisation normalises a mini-batch of activations: "
        "x_hat = (x - mu_B) / sqrt(sigma_B^2 + epsilon), "
        "y = gamma * x_hat + beta, where mu_B and sigma_B^2 are the "
        "batch mean and variance, gamma and beta are learnable parameters, "
        "and epsilon is a small constant for numerical stability."
    ),
    example=(
        "Batch [1, 2, 3, 4], gamma=1, beta=0, eps=1e-5: "
        "mu=2.5, var=1.25. x_hat = [-1.342, -0.447, 0.447, 1.342]. "
        "y = x_hat (since gamma=1, beta=0)."
    ),
    tier=5,
    domain="machine_learning",
    source="Ioffe & Szegedy, 'Batch Normalization', arXiv:1502.03167.",
    source_url="https://en.wikipedia.org/wiki/Batch_normalization",
    prerequisites=["mean", "variance"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="dropout_forward",
    content=(
        "Dropout randomly sets activations to zero during training with "
        "probability p (drop rate), and scales the remaining activations "
        "by 1/(1-p) to maintain expected values (inverted dropout). "
        "At inference, no dropout is applied."
    ),
    example=(
        "x = [1.0, 2.0, 3.0, 4.0], p=0.5, mask=[1,0,1,0]: "
        "output = [1.0/(1-0.5), 0, 3.0/(1-0.5), 0] = [2.0, 0, 6.0, 0]."
    ),
    tier=4,
    domain="machine_learning",
    source="Srivastava et al., 'Dropout', JMLR 2014.",
    source_url="https://en.wikipedia.org/wiki/Dilution_(neural_networks)",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="conv2d_forward",
    content=(
        "2D convolution slides a kernel (filter) over the input, "
        "computing the element-wise product and sum at each position. "
        "For input I of size (H,W) and kernel K of size (kH,kW): "
        "output[i,j] = sum_{m,n} I[i+m, j+n] * K[m, n]. "
        "Output size: ((H-kH+2*pad)/stride + 1, (W-kW+2*pad)/stride + 1)."
    ),
    example=(
        "Input 3x3 = [[1,2,3],[4,5,6],[7,8,9]], kernel 2x2 = [[1,0],[0,1]]: "
        "output[0,0] = 1*1+2*0+4*0+5*1 = 6, output[0,1] = 2+6 = 8, "
        "output[1,0] = 4+8 = 12, output[1,1] = 5+9 = 14. Output = [[6,8],[12,14]]."
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Convolutional neural network', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convolutional_neural_network",
    prerequisites=["dot_product", "matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="max_pool_forward",
    content=(
        "Max pooling reduces spatial dimensions by taking the maximum "
        "value within each pooling window. For a 2x2 pool with stride 2 "
        "on a 4x4 input, each output cell is the max of its 2x2 region."
    ),
    example=(
        "Input 4x4 = [[1,3,2,4],[5,6,1,2],[7,2,3,1],[4,8,5,6]], "
        "pool 2x2, stride 2: output = [[6,4],[8,6]]."
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Convolutional neural network', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convolutional_neural_network#Pooling_layers",
    prerequisites=["comparison"],
))

register_atom(Atom(
    atom_type="formula",
    name="layer_norm_forward",
    content=(
        "Layer normalisation normalises across features for each sample: "
        "x_hat = (x - mu) / sqrt(sigma^2 + epsilon), y = gamma * x_hat + beta, "
        "where mu and sigma^2 are the mean and variance computed over the "
        "feature dimension of a single sample (not the batch)."
    ),
    example=(
        "x = [1, 2, 3], gamma=[1,1,1], beta=[0,0,0], eps=1e-5: "
        "mu=2, var=2/3. x_hat = [-1.2247, 0, 1.2247]. y = x_hat."
    ),
    tier=5,
    domain="machine_learning",
    source="Ba et al., 'Layer Normalization', arXiv:1607.06450.",
    source_url="https://en.wikipedia.org/wiki/Layer_normalization",
    prerequisites=["mean", "variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="gelu_eval",
    content=(
        "The Gaussian Error Linear Unit (GELU) activation is "
        "GELU(x) = x * Phi(x), where Phi(x) is the standard normal CDF. "
        "Approximation: GELU(x) ~ 0.5*x*(1 + tanh(sqrt(2/pi)*(x + 0.044715*x^3)))."
    ),
    example="x=1.0: GELU(1.0) = 1.0 * Phi(1.0) = 1.0 * 0.8413 = 0.8413.",
    tier=5,
    domain="machine_learning",
    source="Hendrycks & Gimpel, 'Gaussian Error Linear Units', arXiv:1606.08415.",
    source_url="https://en.wikipedia.org/wiki/Activation_function#Comparison_of_activation_functions",
    prerequisites=["sigmoid_eval"],
))

register_atom(Atom(
    atom_type="formula",
    name="positional_encoding_eval",
    content=(
        "Sinusoidal positional encoding adds position information to "
        "token embeddings: PE(pos, 2i) = sin(pos / 10000^{2i/d_model}), "
        "PE(pos, 2i+1) = cos(pos / 10000^{2i/d_model}), where pos is "
        "the position and i is the dimension index."
    ),
    example=(
        "pos=0, d_model=4: PE(0,0) = sin(0/10000^0) = sin(0) = 0, "
        "PE(0,1) = cos(0) = 1, PE(0,2) = sin(0/100) = 0, PE(0,3) = cos(0/100) = 1. "
        "PE = [0, 1, 0, 1]."
    ),
    tier=5,
    domain="machine_learning",
    source="Vaswani et al., 'Attention Is All You Need', NeurIPS 2017.",
    source_url="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)",
    prerequisites=["trigonometry"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="multi_head_attention_forward",
    content=(
        "Multi-head attention splits queries, keys, values into h heads, "
        "applies scaled dot-product attention to each, then concatenates "
        "and projects: MultiHead(Q,K,V) = Concat(head_1,...,head_h)*W_O, "
        "where head_i = Attention(Q*W_Q^i, K*W_K^i, V*W_V^i) and "
        "Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V."
    ),
    example=(
        "d_model=4, h=2, d_k=2. Q=K=V=[1,0,1,0]. "
        "Split: Q1=[1,0], Q2=[1,0]. "
        "Score = Q1*K1^T/sqrt(2) = 1/1.414 = 0.707. "
        "Attention weights after softmax: [1.0]. head_1 = V1 = [1,0]."
    ),
    tier=6,
    domain="machine_learning",
    source="Vaswani et al., 'Attention Is All You Need', NeurIPS 2017.",
    source_url="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)#Scaled_dot-product_attention",
    prerequisites=["softmax_eval", "matrix_multiply"],
))

register_atom(Atom(
    atom_type="formula",
    name="embedding_lookup",
    content=(
        "An embedding layer maps discrete token indices to dense vectors. "
        "Given embedding matrix E of shape (vocab_size, d_model), "
        "the output for token index i is E[i], the i-th row of E."
    ),
    example=(
        "E = [[0.1,0.2],[0.3,0.4],[0.5,0.6]], token index 2: "
        "output = E[2] = [0.5, 0.6]."
    ),
    tier=4,
    domain="machine_learning",
    source="Wikipedia contributors, 'Word embedding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Word_embedding",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="residual_connection",
    content=(
        "A residual (skip) connection adds the input of a layer to its "
        "output: y = F(x) + x, where F is the layer transformation. "
        "This allows gradients to flow directly through the identity "
        "path, mitigating vanishing gradients in deep networks."
    ),
    example=(
        "x = [1, 2, 3], F(x) = [0.1, -0.2, 0.3]: "
        "y = [1.1, 1.8, 3.3]."
    ),
    tier=4,
    domain="machine_learning",
    source="He et al., 'Deep Residual Learning', CVPR 2016.",
    source_url="https://en.wikipedia.org/wiki/Residual_neural_network",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="transformer_block_forward",
    content=(
        "A transformer block applies: (1) multi-head self-attention with "
        "residual connection and layer norm, (2) feed-forward network "
        "(two linear layers with activation) with residual and layer norm. "
        "y1 = LayerNorm(x + MultiHead(x,x,x)), "
        "y2 = LayerNorm(y1 + FFN(y1))."
    ),
    example=(
        "Input x = [1,0,1,0], d_model=4. After attention + residual: "
        "y1 = LayerNorm([1,0,1,0] + attn_output). After FFN + residual: "
        "y2 = LayerNorm(y1 + FFN(y1))."
    ),
    tier=6,
    domain="machine_learning",
    source="Vaswani et al., 'Attention Is All You Need', NeurIPS 2017.",
    source_url="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)",
    prerequisites=["multi_head_attention_forward", "layer_norm_forward", "residual_connection"],
))


# =========================================================================
# Computational Geometry (tier 3-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="triangle_centroid",
    content=(
        "The centroid of a triangle with vertices (x1,y1), (x2,y2), "
        "(x3,y3) is the arithmetic mean of the vertices: "
        "G = ((x1+x2+x3)/3, (y1+y2+y3)/3). The centroid divides "
        "each median in ratio 2:1 from vertex to midpoint."
    ),
    example=(
        "Vertices (0,0), (6,0), (3,6): "
        "G = ((0+6+3)/3, (0+0+6)/3) = (3, 2)."
    ),
    tier=3,
    domain="geometry",
    source="Wikipedia contributors, 'Centroid', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Centroid#Of_a_triangle",
    prerequisites=["mean"],
))

register_atom(Atom(
    atom_type="formula",
    name="triangle_circumcenter",
    content=(
        "The circumcenter of a triangle is equidistant from all three "
        "vertices. It is the intersection of the perpendicular bisectors "
        "of the sides. For a triangle with vertices A, B, C, the "
        "circumcenter can be found by solving the system of equations "
        "|PA|^2 = |PB|^2 = |PC|^2."
    ),
    example=(
        "Vertices (0,0), (4,0), (0,3): midpoint AB=(2,0), midpoint AC=(0,1.5). "
        "Perp bisector of AB: x=2. Perp bisector of AC: y=1.5. "
        "Circumcenter = (2, 1.5). Radius = sqrt(4+2.25) = 2.5."
    ),
    tier=4,
    domain="geometry",
    source="Wikipedia contributors, 'Circumscribed circle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Circumscribed_circle",
    prerequisites=["distance_2d", "line_intersection"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="circle_from_three_points",
    content=(
        "Given three non-collinear points, a unique circle passes through "
        "all three. The center is the circumcenter of the triangle formed "
        "by the points. The radius is the distance from the center to "
        "any of the three points."
    ),
    example=(
        "Points (0,0), (4,0), (0,3): circumcenter = (2, 1.5), "
        "radius = sqrt((2-0)^2 + (1.5-0)^2) = sqrt(6.25) = 2.5. "
        "Circle: (x-2)^2 + (y-1.5)^2 = 6.25."
    ),
    tier=4,
    domain="geometry",
    source="Wikipedia contributors, 'Circumscribed circle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Circumscribed_circle",
    prerequisites=["triangle_circumcenter"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="line_circle_intersection",
    content=(
        "To find the intersection of line ax + by + c = 0 with circle "
        "(x-h)^2 + (y-k)^2 = r^2, substitute the line equation into "
        "the circle equation to get a quadratic in one variable. "
        "The discriminant D determines: D > 0 (two points), D = 0 "
        "(tangent), D < 0 (no intersection)."
    ),
    example=(
        "Circle x^2+y^2=25, line y=3: x^2+9=25, x^2=16, x=+/-4. "
        "Intersections: (4,3) and (-4,3)."
    ),
    tier=4,
    domain="geometry",
    source="Wikipedia contributors, 'Line-circle intersection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Intersection_(geometry)#A_line_and_a_circle",
    prerequisites=["quadratic", "distance_2d"],
))

register_atom(Atom(
    atom_type="formula",
    name="polygon_perimeter",
    content=(
        "The perimeter of a polygon with vertices (x1,y1), ..., (xn,yn) "
        "is the sum of the distances between consecutive vertices: "
        "P = sum_{i=1}^{n} sqrt((x_{i+1}-x_i)^2 + (y_{i+1}-y_i)^2), "
        "where vertex n+1 wraps to vertex 1."
    ),
    example=(
        "Square (0,0),(3,0),(3,3),(0,3): sides = 3+3+3+3 = 12."
    ),
    tier=3,
    domain="geometry",
    source="Wikipedia contributors, 'Perimeter', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Perimeter",
    prerequisites=["distance_2d"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="convex_hull_area",
    content=(
        "The convex hull of a set of points is the smallest convex polygon "
        "containing all points. Its area can be computed using the shoelace "
        "formula on the hull vertices in order: "
        "A = 0.5 * |sum(x_i*y_{i+1} - x_{i+1}*y_i)|."
    ),
    example=(
        "Points (0,0),(4,0),(4,3),(0,3),(2,1): hull = (0,0),(4,0),(4,3),(0,3). "
        "Shoelace: |0*0-4*0 + 4*3-4*0 + 4*3-0*3 + 0*0-0*3| / 2 = "
        "|0+12+12+0| / 2 = 12."
    ),
    tier=5,
    domain="geometry",
    source="Wikipedia contributors, 'Convex hull', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convex_hull",
    prerequisites=["polygon_area"],
))

register_atom(Atom(
    atom_type="formula",
    name="regular_polygon_angle",
    content=(
        "The interior angle of a regular n-gon is (n-2)*180/n degrees. "
        "The exterior angle is 360/n degrees. The sum of interior "
        "angles is (n-2)*180 degrees."
    ),
    example=(
        "Regular hexagon (n=6): interior angle = (6-2)*180/6 = 720/6 = 120 degrees. "
        "Exterior angle = 360/6 = 60 degrees."
    ),
    tier=3,
    domain="geometry",
    source="Wikipedia contributors, 'Regular polygon', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Regular_polygon",
    prerequisites=["angle_sum_triangle"],
))

register_atom(Atom(
    atom_type="theorem",
    name="cyclic_quadrilateral",
    content=(
        "A cyclic quadrilateral has all four vertices on a circle. "
        "Its opposite angles sum to 180 degrees: A + C = 180, B + D = 180. "
        "The area is given by Brahmagupta's formula: "
        "K = sqrt((s-a)(s-b)(s-c)(s-d)), where s = (a+b+c+d)/2."
    ),
    example=(
        "Sides a=3, b=4, c=5, d=6: s = (3+4+5+6)/2 = 9. "
        "K = sqrt((9-3)(9-4)(9-5)(9-6)) = sqrt(6*5*4*3) = sqrt(360) = 18.97."
    ),
    tier=5,
    domain="geometry",
    source="Wikipedia contributors, 'Cyclic quadrilateral', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cyclic_quadrilateral",
    prerequisites=["area_triangle"],
))

register_atom(Atom(
    atom_type="theorem",
    name="power_of_point",
    content=(
        "The power of a point P with respect to a circle with center O "
        "and radius r is h(P) = |PO|^2 - r^2. If P is outside the circle, "
        "the power equals the product of signed distances to intersection "
        "points along any line through P."
    ),
    example=(
        "Circle center (0,0), r=5. Point P=(8,0): "
        "power = 8^2 - 5^2 = 64 - 25 = 39. "
        "Line through P along x-axis: intersections at (5,0) and (-5,0). "
        "Product: (8-5)*(8-(-5)) = 3*13 = 39."
    ),
    tier=5,
    domain="geometry",
    source="Wikipedia contributors, 'Power of a point', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Power_of_a_point",
    prerequisites=["distance_2d"],
))

register_atom(Atom(
    atom_type="definition",
    name="radical_axis",
    content=(
        "The radical axis of two circles is the locus of points having "
        "equal power with respect to both circles. For circles "
        "x^2+y^2+D1*x+E1*y+F1=0 and x^2+y^2+D2*x+E2*y+F2=0, "
        "the radical axis is (D1-D2)*x + (E1-E2)*y + (F1-F2) = 0."
    ),
    example=(
        "Circle 1: x^2+y^2=25 (center 0,0, r=5). "
        "Circle 2: (x-6)^2+y^2=9, i.e. x^2+y^2-12x+27=0. "
        "Radical axis: 0-(-12)x + 0 + 0-27+25 = 0 -> 12x - 2 = 0 -> x = 1/6."
    ),
    tier=6,
    domain="geometry",
    source="Wikipedia contributors, 'Radical axis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Radical_axis",
    prerequisites=["power_of_point"],
))

register_atom(Atom(
    atom_type="formula",
    name="spherical_distance",
    content=(
        "The great-circle distance between two points on a sphere of "
        "radius R with coordinates (lat1, lon1) and (lat2, lon2) is: "
        "d = R * arccos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon2-lon1)). "
        "This is the shortest path along the surface (geodesic)."
    ),
    example=(
        "London (51.5N, 0.0W) to New York (40.7N, 74.0W), R=6371km: "
        "d = 6371 * arccos(sin51.5*sin40.7 + cos51.5*cos40.7*cos74) = "
        "6371 * arccos(0.5109 + 0.1412) = 6371 * arccos(0.6521) = "
        "6371 * 0.8607 = 5483 km."
    ),
    tier=5,
    domain="geometry",
    source="Wikipedia contributors, 'Great-circle distance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Great-circle_distance",
    prerequisites=["trigonometry"],
))

register_atom(Atom(
    atom_type="formula",
    name="solid_angle",
    content=(
        "The solid angle subtended by a surface S at a point P is "
        "Omega = integral of (r_hat . dA) / r^2 over S, measured in "
        "steradians (sr). A full sphere subtends 4*pi sr. A cone with "
        "half-angle theta subtends Omega = 2*pi*(1 - cos(theta))."
    ),
    example=(
        "Cone with half-angle 60 degrees: "
        "Omega = 2*pi*(1 - cos(60)) = 2*pi*(1 - 0.5) = pi sr = 3.1416 sr."
    ),
    tier=5,
    domain="geometry",
    source="Wikipedia contributors, 'Solid angle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Solid_angle",
    prerequisites=["trigonometry"],
))


# =========================================================================
# Open Problems / Famous Sequences (tier 7-8)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="zeta_partial_sum",
    content=(
        "The Riemann zeta function is zeta(s) = sum_{n=1}^{infinity} 1/n^s "
        "for Re(s) > 1. The partial sum to N terms approximates the full "
        "value. At s=2: zeta(2) = pi^2/6 = 1.6449..."
    ),
    example=(
        "zeta(2) partial sum to N=4: "
        "1/1 + 1/4 + 1/9 + 1/16 = 1 + 0.25 + 0.1111 + 0.0625 = 1.4236."
    ),
    tier=7,
    domain="number_theory",
    source="Wikipedia contributors, 'Riemann zeta function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Riemann_zeta_function",
    prerequisites=["summation", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="euler_product",
    content=(
        "The Euler product formula expresses the Riemann zeta function "
        "as a product over primes: zeta(s) = product_{p prime} 1/(1-p^{-s}). "
        "This connects the sum over natural numbers to the primes."
    ),
    example=(
        "Partial Euler product for zeta(2) using primes 2,3,5: "
        "1/(1-1/4) * 1/(1-1/9) * 1/(1-1/25) = 4/3 * 9/8 * 25/24 = "
        "900/576 = 1.5625."
    ),
    tier=7,
    domain="number_theory",
    source="Wikipedia contributors, 'Euler product', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euler_product",
    prerequisites=["zeta_partial_sum", "primality"],
))

register_atom(Atom(
    atom_type="theorem",
    name="goldbach_partition",
    content=(
        "Goldbach's conjecture (unproven) states that every even integer "
        "greater than 2 can be expressed as the sum of two primes. "
        "A Goldbach partition of 2n is a pair (p, q) with p + q = 2n "
        "and both p, q prime."
    ),
    example="28 = 5 + 23 = 11 + 17. Both are valid Goldbach partitions.",
    tier=7,
    domain="number_theory",
    source="Wikipedia contributors, 'Goldbach's conjecture', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Goldbach%27s_conjecture",
    prerequisites=["primality"],
))

register_atom(Atom(
    atom_type="definition",
    name="twin_prime_search",
    content=(
        "Twin primes are pairs of primes that differ by 2: (p, p+2). "
        "Examples: (3,5), (5,7), (11,13), (17,19), (29,31). "
        "The twin prime conjecture states there are infinitely many."
    ),
    example=(
        "Find twin primes up to 50: (3,5), (5,7), (11,13), (17,19), "
        "(29,31), (41,43). Total: 6 pairs."
    ),
    tier=7,
    domain="number_theory",
    source="Wikipedia contributors, 'Twin prime', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Twin_prime",
    prerequisites=["primality"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="collatz_longest",
    content=(
        "The Collatz sequence for n: if n is even, next = n/2; if odd, "
        "next = 3n+1. The conjecture states all sequences reach 1. "
        "The stopping time is the number of steps to reach 1."
    ),
    example=(
        "n=6: 6->3->10->5->16->8->4->2->1. Stopping time = 8 steps. "
        "n=7: 7->22->11->34->17->52->26->13->40->20->10->5->16->8->4->2->1. "
        "Stopping time = 16 steps."
    ),
    tier=7,
    domain="number_theory",
    source="Wikipedia contributors, 'Collatz conjecture', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Collatz_conjecture",
    prerequisites=["modular", "division"],
))

register_atom(Atom(
    atom_type="definition",
    name="perfect_number_check",
    content=(
        "A perfect number equals the sum of its proper divisors. "
        "Euclid proved that 2^{p-1}(2^p - 1) is perfect when 2^p - 1 "
        "is prime (a Mersenne prime). Known perfect numbers: "
        "6, 28, 496, 8128, ..."
    ),
    example="28: divisors = 1, 2, 4, 7, 14. Sum = 1+2+4+7+14 = 28. Perfect.",
    tier=7,
    domain="number_theory",
    source="Wikipedia contributors, 'Perfect number', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Perfect_number",
    prerequisites=["factorisation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="abc_conjecture_example",
    content=(
        "The abc conjecture relates the prime factors of a, b, and c = a+b "
        "where gcd(a,b) = 1. The radical rad(abc) = product of distinct "
        "primes dividing abc. The conjecture: for any epsilon > 0, there "
        "are finitely many triples with c > rad(abc)^{1+epsilon}."
    ),
    example=(
        "a=1, b=8=2^3, c=9=3^2. gcd(1,8)=1. "
        "rad(1*8*9) = rad(72) = 2*3 = 6. "
        "c=9 > rad=6, quality q = log(9)/log(6) = 1.226."
    ),
    tier=8,
    domain="number_theory",
    source="Wikipedia contributors, 'abc conjecture', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Abc_conjecture",
    prerequisites=["gcd", "factorisation"],
))

register_atom(Atom(
    atom_type="definition",
    name="prime_gap",
    content=(
        "A prime gap is the difference between consecutive primes: "
        "g_n = p_{n+1} - p_n. The first prime gaps: 1 (2,3), 2 (3,5), "
        "2 (5,7), 4 (7,11), 2 (11,13). The prime number theorem implies "
        "average gap near p is approximately ln(p)."
    ),
    example=(
        "Primes near 100: 97, 101, 103, 107, 109, 113. "
        "Gaps: 4, 2, 4, 2, 4. Average = 3.2. ln(100) = 4.6."
    ),
    tier=7,
    domain="number_theory",
    source="Wikipedia contributors, 'Prime gap', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Prime_gap",
    prerequisites=["primality"],
))

register_atom(Atom(
    atom_type="definition",
    name="mersenne_prime_check",
    content=(
        "A Mersenne prime is a prime of the form M_p = 2^p - 1, where p "
        "itself must be prime (necessary but not sufficient). "
        "Known Mersenne primes: M_2=3, M_3=7, M_5=31, M_7=127, "
        "M_13=8191, ... The Lucas-Lehmer test efficiently checks primality."
    ),
    example=(
        "p=7: M_7 = 2^7 - 1 = 127. Is 127 prime? "
        "Not divisible by 2,3,5,7,11 (sqrt(127)<12). Yes, 127 is a Mersenne prime."
    ),
    tier=7,
    domain="number_theory",
    source="Wikipedia contributors, 'Mersenne prime', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mersenne_prime",
    prerequisites=["exponentiation", "primality"],
))

register_atom(Atom(
    atom_type="definition",
    name="happy_number",
    content=(
        "A happy number is defined by repeatedly summing the squares of "
        "its digits. If the sequence reaches 1, the number is happy; "
        "otherwise it enters a cycle (containing 4) and is unhappy."
    ),
    example=(
        "n=23: 2^2+3^2 = 4+9 = 13. 1^2+3^2 = 1+9 = 10. "
        "1^2+0^2 = 1. Reached 1, so 23 is happy."
    ),
    tier=7,
    domain="number_theory",
    source="Wikipedia contributors, 'Happy number', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Happy_number",
    prerequisites=["digit_root"],
))

register_atom(Atom(
    atom_type="definition",
    name="palindrome_prime",
    content=(
        "A palindromic prime is a prime number that is also a palindrome "
        "(reads the same forwards and backwards). Examples: 2, 3, 5, 7, "
        "11, 101, 131, 151, 181, 191, 313, 353, ..."
    ),
    example=(
        "Is 131 a palindromic prime? 131 reversed = 131 (palindrome). "
        "131 / 2,3,5,7,11: not divisible (sqrt(131)<12). Yes."
    ),
    tier=7,
    domain="number_theory",
    source="Wikipedia contributors, 'Palindromic prime', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Palindromic_prime",
    prerequisites=["primality", "string_reverse"],
))

register_atom(Atom(
    atom_type="definition",
    name="riemann_hypothesis_zero",
    content=(
        "The Riemann hypothesis states that all non-trivial zeros of the "
        "Riemann zeta function have real part 1/2. The trivial zeros are "
        "at s = -2, -4, -6, ... The non-trivial zeros are computed "
        "numerically on the critical line Re(s) = 1/2."
    ),
    example=(
        "First non-trivial zero: s = 0.5 + 14.1347i. "
        "zeta(0.5 + 14.1347i) = 0 (approximately). "
        "Verified for the first 10^13 zeros -- all on Re(s) = 1/2."
    ),
    tier=8,
    domain="number_theory",
    source="Wikipedia contributors, 'Riemann hypothesis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Riemann_hypothesis",
    prerequisites=["zeta_partial_sum", "complex_analysis"],
))
