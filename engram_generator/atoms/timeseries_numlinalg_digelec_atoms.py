"""Knowledge atoms for time series, numerical linear algebra, and digital electronics."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Time series analysis (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="autocorrelation",
    content=(
        "The autocorrelation function at lag k measures the linear "
        "dependence between observations k steps apart: "
        "r_k = sum_{t=1}^{n-k} (x_t - x_bar)(x_{t+k} - x_bar) / "
        "sum_{t=1}^{n} (x_t - x_bar)^2. Values near 1 or -1 indicate "
        "strong serial dependence."
    ),
    example=(
        "Series [2, 4, 6, 8, 10], mean=6. r_1 = (sum of products at lag 1) / "
        "(sum of squared deviations) = 40/40 = 1.0 (perfect linear trend)."
    ),
    tier=5,
    domain="time_series",
    source="Wikipedia contributors, 'Autocorrelation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Autocorrelation",
    prerequisites=["variance"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="exponential_smoothing",
    content=(
        "Simple exponential smoothing forecasts by weighting recent "
        "observations more heavily: s_t = alpha * x_t + (1 - alpha) * s_{t-1}, "
        "where alpha in (0, 1) is the smoothing parameter. The forecast "
        "for future periods is the last smoothed value."
    ),
    example=(
        "alpha=0.3, observations [10, 12, 11, 14]. s_0=10. "
        "s_1=0.3*12 + 0.7*10=10.6. s_2=0.3*11+0.7*10.6=10.72. "
        "s_3=0.3*14+0.7*10.72=11.70."
    ),
    tier=5,
    domain="time_series",
    source="Wikipedia contributors, 'Exponential smoothing', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exponential_smoothing",
    prerequisites=["weighted_sum"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="moving_average",
    content=(
        "A simple moving average of window size k smooths a time series: "
        "MA_t = (x_t + x_{t-1} + ... + x_{t-k+1}) / k. It removes "
        "short-term fluctuations while preserving longer-term trends. "
        "The output has n - k + 1 values."
    ),
    example=(
        "Series [4, 1, 9, 8, 8], k=2: "
        "MA = [(4+1)/2, (1+9)/2, (9+8)/2, (8+8)/2] = [2.5, 5.0, 8.5, 8.0]."
    ),
    tier=5,
    domain="time_series",
    source="Wikipedia contributors, 'Moving average', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Moving_average",
    prerequisites=["arithmetic_mean"],
))

register_atom(Atom(
    atom_type="concept",
    name="arima_forecast",
    content=(
        "ARIMA(p, d, q) combines autoregression (AR), differencing (I), "
        "and moving average (MA). The model for the d-th difference "
        "y_t = diff^d(x_t) is: y_t = c + sum_{i=1}^p phi_i y_{t-i} + "
        "sum_{j=1}^q theta_j e_{t-j} + e_t, where e_t is white noise."
    ),
    example=(
        "ARIMA(1,0,0) = AR(1): y_t = 0.5 + 0.8*y_{t-1} + e_t. "
        "If y_3 = 10, forecast y_4 = 0.5 + 0.8*10 = 8.5."
    ),
    tier=6,
    domain="time_series",
    source="Wikipedia contributors, 'Autoregressive integrated moving average', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average",
    prerequisites=["autocorrelation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="seasonal_decompose",
    content=(
        "Seasonal decomposition splits a time series into trend (T), "
        "seasonal (S), and residual (R) components. Additive model: "
        "x_t = T_t + S_t + R_t. Multiplicative: x_t = T_t * S_t * R_t. "
        "Moving average smoothing extracts the trend, seasonal indices "
        "are averaged across periods."
    ),
    example=(
        "Quarterly data [100, 120, 80, 110, 105, 125, 85, 115]. "
        "Trend via 4-period MA. Detrended values give seasonal indices. "
        "S = [-7.5, 17.5, -22.5, 12.5] (quarterly pattern)."
    ),
    tier=5,
    domain="time_series",
    source="Wikipedia contributors, 'Decomposition of time series', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Decomposition_of_time_series",
    prerequisites=["moving_average"],
))

register_atom(Atom(
    atom_type="concept",
    name="stationarity_check",
    content=(
        "A time series is stationary if its statistical properties "
        "(mean, variance, autocorrelation) do not change over time. "
        "The augmented Dickey-Fuller (ADF) test checks for a unit root: "
        "delta_y_t = alpha + beta*t + gamma*y_{t-1} + ... + e_t. "
        "Reject H0 (unit root) if test statistic < critical value."
    ),
    example=(
        "ADF test statistic = -3.45, 5% critical value = -2.86. "
        "|-3.45| > |-2.86|, so reject H0: the series is stationary."
    ),
    tier=5,
    domain="time_series",
    source="Wikipedia contributors, 'Augmented Dickey-Fuller test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Augmented_Dickey%E2%80%93Fuller_test",
    prerequisites=["hypothesis_test"],
))

# ---------------------------------------------------------------------------
# Numerical linear algebra (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="qr_decomposition",
    content=(
        "QR decomposition factors a matrix A into Q (orthogonal) and "
        "R (upper triangular): A = QR. Gram-Schmidt orthogonalisation "
        "constructs Q column by column. Used for least squares, "
        "eigenvalue algorithms, and solving linear systems."
    ),
    example=(
        "A = [[1,1],[1,0]]. u1 = [1,1]/sqrt(2). "
        "u2 = [1,0] - proj = [0.5,-0.5]/sqrt(0.5). "
        "Q = [[0.707,0.707],[0.707,-0.707]], R = [[1.414,0.707],[0,0.707]]."
    ),
    tier=6,
    domain="numerical_linear_algebra",
    source="Wikipedia contributors, 'QR decomposition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/QR_decomposition",
    prerequisites=["gram_schmidt"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="svd_compute",
    content=(
        "The singular value decomposition factors A = U * Sigma * V^T, "
        "where U and V are orthogonal and Sigma is diagonal with "
        "non-negative singular values. The rank of A equals the number "
        "of non-zero singular values. SVD is used for dimensionality "
        "reduction (PCA), pseudoinverse, and low-rank approximation."
    ),
    example=(
        "A = [[3,0],[0,4]]. Singular values: sigma_1=4, sigma_2=3. "
        "U = [[0,1],[1,0]], Sigma = [[4,0],[0,3]], V^T = [[0,1],[1,0]]."
    ),
    tier=6,
    domain="numerical_linear_algebra",
    source="Wikipedia contributors, 'Singular value decomposition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Singular_value_decomposition",
    prerequisites=["eigenvalue"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="cholesky_factor",
    content=(
        "Cholesky decomposition factors a symmetric positive-definite "
        "matrix A as A = L * L^T, where L is lower triangular. "
        "L_{jj} = sqrt(A_{jj} - sum_{k<j} L_{jk}^2). It is twice as "
        "fast as LU decomposition and numerically stable."
    ),
    example=(
        "A = [[4,2],[2,5]]. L_{11}=sqrt(4)=2. L_{21}=2/2=1. "
        "L_{22}=sqrt(5-1)=2. L = [[2,0],[1,2]]."
    ),
    tier=6,
    domain="numerical_linear_algebra",
    source="Wikipedia contributors, 'Cholesky decomposition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cholesky_decomposition",
    prerequisites=["determinant"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="jacobi_iteration",
    content=(
        "Jacobi iteration solves Ax = b by decomposing A = D + R, "
        "then iterating x^{k+1} = D^{-1}(b - R*x^k). Each component: "
        "x_i^{k+1} = (b_i - sum_{j!=i} a_{ij}*x_j^k) / a_{ii}. "
        "Converges when A is diagonally dominant."
    ),
    example=(
        "A = [[4,1],[1,3]], b = [1,2]. x^0 = [0,0]. "
        "x^1 = [1/4, 2/3] = [0.25, 0.667]. "
        "x^2 = [(1-0.667)/4, (2-0.25)/3] = [0.083, 0.583]."
    ),
    tier=5,
    domain="numerical_linear_algebra",
    source="Wikipedia contributors, 'Jacobi method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Jacobi_method",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="gauss_seidel",
    content=(
        "Gauss-Seidel iteration improves on Jacobi by using updated "
        "values as soon as they are computed: "
        "x_i^{k+1} = (b_i - sum_{j<i} a_{ij}*x_j^{k+1} - sum_{j>i} a_{ij}*x_j^k) / a_{ii}. "
        "Typically converges faster than Jacobi for the same system."
    ),
    example=(
        "A = [[4,1],[1,3]], b = [1,2]. x^0 = [0,0]. "
        "x_1^1 = 1/4 = 0.25. x_2^1 = (2-0.25)/3 = 0.583. "
        "(Used x_1^1 immediately for x_2^1, unlike Jacobi.)"
    ),
    tier=5,
    domain="numerical_linear_algebra",
    source="Wikipedia contributors, 'Gauss-Seidel method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gauss%E2%80%93Seidel_method",
    prerequisites=["jacobi_iteration"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="least_squares",
    content=(
        "The least squares solution minimises ||Ax - b||^2. The normal "
        "equations A^T A x = A^T b give x = (A^T A)^{-1} A^T b. "
        "QR decomposition provides a more numerically stable approach: "
        "Rx = Q^T b."
    ),
    example=(
        "A = [[1,1],[1,2],[1,3]], b = [1,2,4]. "
        "A^T A = [[3,6],[6,14]], A^T b = [7,17]. "
        "x = [[-1],[1.5]]: y = -1 + 1.5x."
    ),
    tier=6,
    domain="numerical_linear_algebra",
    source="Wikipedia contributors, 'Least squares', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Least_squares",
    prerequisites=["qr_decomposition"],
))

# ---------------------------------------------------------------------------
# Digital electronics (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="karnaugh_map",
    content=(
        "A Karnaugh map (K-map) is a graphical method for simplifying "
        "Boolean functions. Minterms are arranged in a grid using Gray "
        "code ordering so adjacent cells differ by one variable. Groups "
        "of 1s (size 2^k) correspond to simplified product terms."
    ),
    example=(
        "F(A,B) with minterms {1,2,3}: K-map [[0,1],[1,1]]. "
        "Group row 2: A. Group column 2: B. F = A + B."
    ),
    tier=4,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Karnaugh map', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Karnaugh_map",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="concept",
    name="flip_flop_state",
    content=(
        "A flip-flop is a bistable circuit that stores one bit. A D "
        "flip-flop captures input D on the clock edge: Q_next = D. "
        "A JK flip-flop: Q_next = J*Q' + K'*Q. A T (toggle) flip-flop: "
        "Q_next = T XOR Q."
    ),
    example=(
        "D flip-flop, inputs D = [1, 0, 1, 1], Q_0 = 0: "
        "Q = [1, 0, 1, 1] (captures D on each clock edge)."
    ),
    tier=4,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Flip-flop (electronics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Flip-flop_(electronics)",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="concept",
    name="timing_analysis",
    content=(
        "Static timing analysis determines the maximum clock frequency "
        "of a digital circuit. The critical path is the longest "
        "combinational delay between flip-flops: T_clk >= T_cq + T_comb + T_su, "
        "where T_cq is clock-to-Q delay, T_comb is combinational delay, "
        "and T_su is setup time."
    ),
    example=(
        "T_cq = 0.5 ns, T_comb = 3.2 ns, T_su = 0.3 ns. "
        "T_clk >= 0.5 + 3.2 + 0.3 = 4.0 ns. f_max = 250 MHz."
    ),
    tier=5,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Static timing analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Static_timing_analysis",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="adder_circuit",
    content=(
        "A full adder computes the sum of two bits plus carry-in: "
        "S = A XOR B XOR C_in, C_out = (A AND B) OR (C_in AND (A XOR B)). "
        "An n-bit ripple-carry adder chains n full adders. The carry "
        "propagates through all stages in the worst case."
    ),
    example=(
        "A=1, B=1, C_in=0: S = 1^1^0 = 0, C_out = (1&1)|(0&0) = 1. "
        "4-bit: 1011 + 0110 = 10001 (11 + 6 = 17)."
    ),
    tier=4,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Adder (electronics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Adder_(electronics)",
    prerequisites=["binary_arithmetic"],
))

register_atom(Atom(
    atom_type="concept",
    name="counter_design",
    content=(
        "A binary counter increments by 1 on each clock pulse using "
        "cascaded flip-flops. An n-bit counter counts from 0 to 2^n - 1. "
        "Synchronous counters update all bits simultaneously; "
        "asynchronous (ripple) counters propagate changes sequentially."
    ),
    example=(
        "3-bit synchronous counter: states 000, 001, 010, 011, 100, "
        "101, 110, 111, 000... T flip-flop at bit i toggles when "
        "all lower bits are 1."
    ),
    tier=5,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Counter (digital)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Counter_(digital)",
    prerequisites=["flip_flop_state"],
))

register_atom(Atom(
    atom_type="concept",
    name="multiplexer",
    content=(
        "A multiplexer (MUX) selects one of 2^n input lines using n "
        "select lines: Y = sum_{i=0}^{2^n-1} I_i * m_i, where m_i is "
        "the minterm of the select inputs. A 4:1 MUX: "
        "Y = I0*S1'S0' + I1*S1'S0 + I2*S1*S0' + I3*S1*S0."
    ),
    example=(
        "4:1 MUX, inputs [1, 0, 1, 0], select S1=1, S0=0: "
        "Y = I2 = 1 (selects input 2)."
    ),
    tier=4,
    domain="digital_electronics",
    source="Wikipedia contributors, 'Multiplexer', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Multiplexer",
    prerequisites=["boolean_eval"],
))
