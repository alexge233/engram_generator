"""Knowledge atoms for ML operations and computational geometry.

Covers neural network layer operations (ReLU, batch norm, dropout,
convolution, attention) and computational geometry (centroid,
circumcenter, projections, transformations, conics).
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Machine Learning -- layer operations
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="relu_derivative",
    content=(
        "The Rectified Linear Unit (ReLU) activation function is defined as "
        "f(x) = max(0, x). Its derivative is f'(x) = 1 if x > 0, and "
        "f'(x) = 0 if x < 0. The derivative is undefined at x = 0 but is "
        "conventionally set to 0 or 1 in practice. ReLU is the most widely "
        "used activation function in deep learning due to its computational "
        "simplicity and its ability to mitigate the vanishing gradient problem."
    ),
    example=(
        "Given x = [-2, 0, 3, -1, 5]: "
        "ReLU(x) = [0, 0, 3, 0, 5]; "
        "ReLU'(x) = [0, 0, 1, 0, 1]"
    ),
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
        "Batch Normalisation normalises each feature across a mini-batch to "
        "have zero mean and unit variance, then applies a learned affine "
        "transform: y = gamma * (x - mu_B) / sqrt(sigma_B^2 + epsilon) + beta, "
        "where mu_B is the batch mean, sigma_B^2 is the batch variance, "
        "gamma and beta are learned parameters, and epsilon is a small "
        "constant for numerical stability (typically 1e-5)."
    ),
    example=(
        "Given x = [1, 2, 3, 4], gamma=1, beta=0, eps=0: "
        "mu = 2.5, var = 1.25, "
        "y = (x - 2.5) / sqrt(1.25) = [-1.342, -0.4472, 0.4472, 1.342]"
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Batch normalization', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Batch_normalization",
    prerequisites=["mean", "variance"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="dropout_forward",
    content=(
        "Dropout is a regularisation technique where during training, each "
        "neuron's output is set to zero with probability p (the dropout rate), "
        "and the remaining outputs are scaled by 1/(1-p) to maintain the "
        "expected value. During inference, dropout is not applied. "
        "This prevents co-adaptation of neurons and acts as an approximate "
        "ensemble method."
    ),
    example=(
        "Given x = [2.0, 4.0, 6.0], p=0.5, mask=[1, 0, 1]: "
        "y = x * mask / (1 - p) = [2.0*1/0.5, 4.0*0/0.5, 6.0*1/0.5] "
        "= [4.0, 0.0, 12.0]"
    ),
    tier=4,
    domain="machine_learning",
    source="Wikipedia contributors, 'Dropout (neural networks)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dropout_(neural_networks)",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="conv2d_forward",
    content=(
        "A 2D convolution slides a kernel (filter) over an input feature map, "
        "computing the element-wise product and sum at each position. For input "
        "of size H x W with kernel K of size k_h x k_w, stride s, and padding p, "
        "the output size is ((H + 2p - k_h) / s + 1) x ((W + 2p - k_w) / s + 1). "
        "Each output element is: y[i,j] = sum_{m,n} x[i*s+m, j*s+n] * K[m,n]."
    ),
    example=(
        "Given 3x3 input [[1,2,3],[4,5,6],[7,8,9]], 2x2 kernel [[1,0],[0,1]], "
        "stride=1, padding=0: output = [[1*1+2*0+4*0+5*1, 2*1+3*0+5*0+6*1], "
        "[4*1+5*0+7*0+8*1, 5*1+6*0+8*0+9*1]] = [[6, 8], [12, 14]]"
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Convolutional neural network', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convolutional_neural_network",
    prerequisites=["matrix_multiply", "addition"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="maxpool_forward",
    content=(
        "Max pooling is a downsampling operation that partitions the input "
        "into non-overlapping rectangular regions and outputs the maximum "
        "value in each region. For a 2D input with pool size k and stride s, "
        "the output at position (i,j) is max(x[i*s:i*s+k, j*s:j*s+k]). "
        "Max pooling provides translational invariance and reduces the spatial "
        "dimensions of feature maps."
    ),
    example=(
        "Given 4x4 input [[1,3,2,4],[5,6,7,8],[9,2,1,3],[4,8,5,6]], "
        "pool_size=2, stride=2: output = [[max(1,3,5,6), max(2,4,7,8)], "
        "[max(9,2,4,8), max(1,3,5,6)]] = [[6, 8], [9, 6]]"
    ),
    tier=4,
    domain="machine_learning",
    source="Wikipedia contributors, 'Convolutional neural network', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convolutional_neural_network#Pooling_layers",
    prerequisites=["comparison"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="embedding_lookup",
    content=(
        "An embedding layer maps discrete tokens (integers) to dense vectors "
        "by table lookup. Given an embedding matrix E of shape (V, d) where "
        "V is vocabulary size and d is embedding dimension, the output for "
        "token index i is E[i], the i-th row of E. During training, the "
        "embedding matrix is updated via backpropagation."
    ),
    example=(
        "Given E = [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]], "
        "input tokens = [2, 0, 1]: "
        "output = [E[2], E[0], E[1]] = [[0.5, 0.6], [0.1, 0.2], [0.3, 0.4]]"
    ),
    tier=3,
    domain="machine_learning",
    source="Wikipedia contributors, 'Word embedding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Word_embedding",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="gelu_compute",
    content=(
        "The Gaussian Error Linear Unit (GELU) activation function is "
        "defined as GELU(x) = x * Phi(x), where Phi(x) is the cumulative "
        "distribution function of the standard normal distribution. An "
        "approximate form is GELU(x) = 0.5*x*(1 + tanh(sqrt(2/pi) * "
        "(x + 0.044715*x^3))). GELU is used in GPT and BERT architectures."
    ),
    example=(
        "Given x = 1.0: GELU(1.0) = 1.0 * Phi(1.0) = 1.0 * 0.8413 = 0.8413. "
        "Given x = -1.0: GELU(-1.0) = -1.0 * Phi(-1.0) = -1.0 * 0.1587 = -0.1587"
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Activation function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Activation_function#Comparison_of_activation_functions",
    prerequisites=["sigmoid_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="cross_attention",
    content=(
        "Cross-attention (or encoder-decoder attention) computes attention "
        "between queries from one sequence and keys/values from another. "
        "Given Q from the decoder (shape [n, d_k]) and K, V from the encoder "
        "(shape [m, d_k] and [m, d_v]): Attention(Q, K, V) = softmax(Q @ K^T "
        "/ sqrt(d_k)) @ V. This allows the decoder to attend to relevant parts "
        "of the encoder output."
    ),
    example=(
        "Given Q=[[1,0]], K=[[1,0],[0,1]], V=[[3],[7]], d_k=2: "
        "scores = [1*1+0*0, 1*0+0*1]/sqrt(2) = [0.707, 0]; "
        "weights = softmax([0.707, 0]) = [0.670, 0.330]; "
        "output = 0.670*3 + 0.330*7 = 4.32"
    ),
    tier=6,
    domain="machine_learning",
    source="Wikipedia contributors, 'Attention (machine learning)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Attention_(machine_learning)",
    prerequisites=["matrix_multiply", "softmax_eval"],
))

register_atom(Atom(
    atom_type="formula",
    name="gradient_clipping",
    content=(
        "Gradient clipping rescales the gradient vector when its norm exceeds "
        "a threshold, preventing exploding gradients during training. Given "
        "gradient g and max norm c: if ||g|| > c, then g_clipped = g * c / ||g||. "
        "Otherwise g_clipped = g. The L2 norm is ||g|| = sqrt(sum(g_i^2))."
    ),
    example=(
        "Given g = [3, 4], max_norm = 2.5: "
        "||g|| = sqrt(9 + 16) = 5.0 > 2.5, "
        "g_clipped = [3, 4] * 2.5 / 5.0 = [1.5, 2.0]"
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Gradient clipping', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gradient_clipping",
    prerequisites=["norm"],
))

register_atom(Atom(
    atom_type="formula",
    name="learning_rate_warmup",
    content=(
        "Learning rate warmup linearly increases the learning rate from a "
        "small value to the target learning rate over a fixed number of "
        "warmup steps. At step t during warmup: lr(t) = lr_target * t / T_warmup, "
        "where T_warmup is the total number of warmup steps. After warmup, "
        "a decay schedule (cosine, linear, or step) is typically applied."
    ),
    example=(
        "Given lr_target = 0.001, T_warmup = 1000, t = 500: "
        "lr(500) = 0.001 * 500 / 1000 = 0.0005"
    ),
    tier=4,
    domain="machine_learning",
    source="Wikipedia contributors, 'Learning rate', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Learning_rate",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="loss_landscape_local",
    content=(
        "Local loss landscape analysis examines the curvature of the loss "
        "function around a point by computing the Hessian matrix H of second "
        "derivatives. The eigenvalues of H indicate: all positive = local "
        "minimum, all negative = local maximum, mixed signs = saddle point. "
        "The condition number kappa = lambda_max / lambda_min indicates "
        "the sharpness of the minimum."
    ),
    example=(
        "Given loss L(w1, w2) = w1^2 + 4*w2^2 at (0,0): "
        "H = [[2, 0], [0, 8]], eigenvalues = [2, 8], "
        "all positive = local minimum, kappa = 8/2 = 4"
    ),
    tier=6,
    domain="machine_learning",
    source="Wikipedia contributors, 'Loss function', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Loss_function",
    prerequisites=["eigenvalue", "gradient"],
))

register_atom(Atom(
    atom_type="formula",
    name="weight_decay_update",
    content=(
        "Weight decay (L2 regularisation) adds a penalty proportional to "
        "the squared magnitude of weights to the loss function. The update "
        "rule becomes: w_{t+1} = w_t - lr * (grad + lambda * w_t), which "
        "is equivalent to: w_{t+1} = (1 - lr * lambda) * w_t - lr * grad, "
        "where lambda is the weight decay coefficient. This shrinks weights "
        "toward zero each step."
    ),
    example=(
        "Given w = 2.0, grad = 0.5, lr = 0.1, lambda = 0.01: "
        "w_new = (1 - 0.1*0.01) * 2.0 - 0.1 * 0.5 "
        "= 0.999 * 2.0 - 0.05 = 1.998 - 0.05 = 1.948"
    ),
    tier=5,
    domain="machine_learning",
    source="Wikipedia contributors, 'Weight decay', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Regularization_(mathematics)#Tikhonov_regularization",
    prerequisites=["multiplication", "subtraction"],
))


# =========================================================================
# Geometry -- computational geometry
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="triangle_centroid",
    content=(
        "The centroid of a triangle with vertices (x1, y1), (x2, y2), "
        "(x3, y3) is the point G = ((x1+x2+x3)/3, (y1+y2+y3)/3). "
        "The centroid is the intersection of the three medians (lines from "
        "each vertex to the midpoint of the opposite side). It divides each "
        "median in the ratio 2:1 from the vertex."
    ),
    example=(
        "Given vertices (0,0), (6,0), (3,9): "
        "G = ((0+6+3)/3, (0+0+9)/3) = (3, 3)"
    ),
    tier=3,
    domain="geometry",
    source="Wikipedia contributors, 'Centroid', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Centroid#Of_a_triangle",
    prerequisites=["addition", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="triangle_circumcenter",
    content=(
        "The circumcenter of a triangle is the point equidistant from all "
        "three vertices; it is the centre of the circumscribed circle. For "
        "a triangle with vertices A, B, C, the circumcenter is found by "
        "solving the system of perpendicular bisector equations. For a "
        "right triangle, the circumcenter is the midpoint of the hypotenuse."
    ),
    example=(
        "Given right triangle (0,0), (4,0), (0,3): "
        "circumcenter = midpoint of hypotenuse = ((4+0)/2, (0+3)/2) = (2, 1.5), "
        "circumradius = distance to any vertex = sqrt(4+2.25) = 2.5"
    ),
    tier=4,
    domain="geometry",
    source="Wikipedia contributors, 'Circumscribed circle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Circumscribed_circle",
    prerequisites=["distance_2d", "midpoint"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="circle_from_three_points",
    content=(
        "Given three non-collinear points, there is exactly one circle passing "
        "through all three. The centre is the circumcenter (intersection of "
        "perpendicular bisectors) and the radius is the distance from the "
        "centre to any of the three points. The general equation of a circle "
        "is (x-h)^2 + (y-k)^2 = r^2."
    ),
    example=(
        "Given points (0,0), (4,0), (0,3): "
        "centre = (2, 1.5) (circumcenter), "
        "r = sqrt((2-0)^2 + (1.5-0)^2) = sqrt(6.25) = 2.5"
    ),
    tier=5,
    domain="geometry",
    source="Wikipedia contributors, 'Circumscribed circle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Circumscribed_circle#Cartesian_coordinates_2",
    prerequisites=["triangle_circumcenter"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="line_circle_intersection",
    content=(
        "To find the intersection of a line y = mx + c with a circle "
        "(x-h)^2 + (y-k)^2 = r^2, substitute the line equation into the "
        "circle equation to obtain a quadratic in x. The discriminant "
        "D = b^2 - 4ac determines: D > 0 two intersections, D = 0 tangent, "
        "D < 0 no intersection."
    ),
    example=(
        "Given circle x^2 + y^2 = 25, line y = x: "
        "x^2 + x^2 = 25, 2x^2 = 25, x = +/-sqrt(12.5) = +/-3.5355; "
        "intersections at (3.5355, 3.5355) and (-3.5355, -3.5355)"
    ),
    tier=4,
    domain="geometry",
    source="Wikipedia contributors, 'Line-sphere intersection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection",
    prerequisites=["quadratic", "distance_2d"],
))

register_atom(Atom(
    atom_type="formula",
    name="vector_projection_2d",
    content=(
        "The scalar projection of vector a onto vector b is "
        "comp_b(a) = (a . b) / ||b||, and the vector projection is "
        "proj_b(a) = ((a . b) / (b . b)) * b. The rejection (component "
        "perpendicular to b) is a - proj_b(a)."
    ),
    example=(
        "Given a = (3, 4), b = (1, 0): "
        "a.b = 3, b.b = 1, proj_b(a) = (3/1)*(1,0) = (3, 0); "
        "rejection = (3,4) - (3,0) = (0, 4)"
    ),
    tier=3,
    domain="geometry",
    source="Wikipedia contributors, 'Vector projection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Vector_projection",
    prerequisites=["dot_product", "norm"],
))

register_atom(Atom(
    atom_type="formula",
    name="rotation_2d",
    content=(
        "A 2D rotation by angle theta about the origin maps point (x, y) to "
        "(x*cos(theta) - y*sin(theta), x*sin(theta) + y*cos(theta)). "
        "The rotation matrix is R = [[cos(theta), -sin(theta)], "
        "[sin(theta), cos(theta)]]. Positive theta is counterclockwise."
    ),
    example=(
        "Given point (1, 0), theta = 90 degrees: "
        "x' = 1*cos(90) - 0*sin(90) = 0, "
        "y' = 1*sin(90) + 0*cos(90) = 1; "
        "result = (0, 1)"
    ),
    tier=4,
    domain="geometry",
    source="Wikipedia contributors, 'Rotation matrix', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rotation_matrix",
    prerequisites=["sin_cos_eval", "matrix_multiply"],
))

register_atom(Atom(
    atom_type="formula",
    name="reflection_line",
    content=(
        "Reflection of a point (x, y) across the line y = mx + c is computed "
        "by finding the perpendicular from the point to the line, then "
        "extending to the same distance on the other side. For reflection "
        "across y = mx: x' = (x(1-m^2) + 2my) / (1+m^2), "
        "y' = (2mx - y(1-m^2)) / (1+m^2)."
    ),
    example=(
        "Given point (3, 1), reflection across y = x (m=1): "
        "x' = (3*(1-1) + 2*1*1)/(1+1) = 2/2 = 1, "
        "y' = (2*1*3 - 1*(1-1))/(1+1) = 6/2 = 3; "
        "result = (1, 3)"
    ),
    tier=4,
    domain="geometry",
    source="Wikipedia contributors, 'Reflection (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Reflection_(mathematics)",
    prerequisites=["distance_2d", "slope"],
))

register_atom(Atom(
    atom_type="formula",
    name="area_polygon_shoelace",
    content=(
        "The shoelace formula computes the area of a simple polygon given "
        "its vertices (x1,y1), ..., (xn,yn) in order: "
        "A = (1/2)|sum_{i=1}^{n}(x_i*y_{i+1} - x_{i+1}*y_i)|, "
        "where indices are taken modulo n. The formula works for any simple "
        "(non-self-intersecting) polygon with vertices listed in order."
    ),
    example=(
        "Given triangle (0,0), (4,0), (0,3): "
        "A = 0.5*|0*0 - 4*0 + 4*3 - 0*0 + 0*0 - 0*3| "
        "= 0.5*|0 + 12 + 0| = 6"
    ),
    tier=4,
    domain="geometry",
    source="Wikipedia contributors, 'Shoelace formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shoelace_formula",
    prerequisites=["multiplication", "subtraction"],
))

register_atom(Atom(
    atom_type="formula",
    name="parametric_line_3d",
    content=(
        "A line in 3D passing through point P0 = (x0, y0, z0) with "
        "direction vector d = (a, b, c) is expressed parametrically as: "
        "r(t) = P0 + t*d = (x0 + at, y0 + bt, z0 + ct). "
        "Two points P0 and P1 give d = P1 - P0. The parameter t = 0 "
        "gives P0 and t = 1 gives P1."
    ),
    example=(
        "Given P0 = (1, 2, 3), P1 = (4, 6, 3): "
        "d = (3, 4, 0); r(t) = (1+3t, 2+4t, 3); "
        "at t=0.5: r = (2.5, 4, 3)"
    ),
    tier=4,
    domain="geometry",
    source="Wikipedia contributors, 'Line (geometry)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Line_(geometry)#In_higher_dimensions",
    prerequisites=["addition", "multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="plane_equation",
    content=(
        "A plane in 3D is defined by the equation ax + by + cz = d, where "
        "n = (a, b, c) is the normal vector. Given three non-collinear points "
        "P1, P2, P3: the normal is n = (P2-P1) x (P3-P1) (cross product). "
        "The distance from a point Q to the plane is "
        "|a*Qx + b*Qy + c*Qz - d| / ||n||."
    ),
    example=(
        "Given points (1,0,0), (0,1,0), (0,0,1): "
        "v1 = (-1,1,0), v2 = (-1,0,1), n = v1 x v2 = (1,1,1); "
        "plane: x + y + z = 1"
    ),
    tier=5,
    domain="geometry",
    source="Wikipedia contributors, 'Plane (geometry)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Plane_(geometry)#Point%E2%80%93normal_form_and_general_form_of_the_equation_of_a_plane",
    prerequisites=["cross_product", "dot_product"],
))

register_atom(Atom(
    atom_type="formula",
    name="distance_point_line",
    content=(
        "The distance from point (x0, y0) to the line ax + by + c = 0 is "
        "d = |a*x0 + b*y0 + c| / sqrt(a^2 + b^2). For a line through "
        "points P1 and P2, the distance from point P0 is "
        "d = |(P2-P1) x (P1-P0)| / |P2-P1|."
    ),
    example=(
        "Given point (3, 4), line 3x + 4y - 5 = 0: "
        "d = |3*3 + 4*4 - 5| / sqrt(9 + 16) = |9 + 16 - 5| / 5 = 20/5 = 4"
    ),
    tier=3,
    domain="geometry",
    source="Wikipedia contributors, 'Distance from a point to a line', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line",
    prerequisites=["absolute_value", "square_root"],
))

register_atom(Atom(
    atom_type="definition",
    name="conic_section",
    content=(
        "A conic section is a curve obtained by intersecting a cone with a "
        "plane. The general equation is Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0. "
        "Classification by discriminant B^2 - 4AC: if < 0 and A = C, B = 0: "
        "circle; if < 0 otherwise: ellipse; if = 0: parabola; if > 0: "
        "hyperbola."
    ),
    example=(
        "Given x^2 + 4y^2 - 4 = 0: A=1, B=0, C=4, "
        "B^2-4AC = 0-16 = -16 < 0 and A != C, "
        "so this is an ellipse: x^2/4 + y^2/1 = 1"
    ),
    tier=5,
    domain="geometry",
    source="Wikipedia contributors, 'Conic section', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conic_section",
    prerequisites=["quadratic"],
))
