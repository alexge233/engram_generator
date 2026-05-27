"""Knowledge atoms for statistics, probability, quantum, and CS domains.

Registers formula atoms covering descriptive statistics, probability
distributions, quantum mechanics, boolean logic, binary arithmetic,
neural networks, and algorithmic complexity. Each atom stores the
canonical LaTeX formula, its tier, domain, and prerequisite atoms.

Physics and astrophysics atoms are registered in atoms/physics.py.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Statistics — descriptive (tier 2-4)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="mean",
    content="\\bar{x} = \\frac{1}{n}\\sum_{i=1}^n x_i",
    tier=2,
    domain="statistics",
    prerequisites=["addition", "division"],
))

register_atom(Atom(
    atom_type="definition",
    name="median",
    content="\\text{median} = \\text{middle value of sorted data}",
    tier=2,
    domain="statistics",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="definition",
    name="mode",
    content="\\text{mode} = \\text{most frequent value}",
    tier=2,
    domain="statistics",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="formula",
    name="variance",
    content="\\sigma^2 = \\frac{1}{n}\\sum_{i=1}^n (x_i - \\bar{x})^2",
    tier=3,
    domain="statistics",
    prerequisites=["mean", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="std_dev",
    content="\\sigma = \\sqrt{\\frac{1}{n}\\sum_{i=1}^n (x_i - \\bar{x})^2}",
    tier=3,
    domain="statistics",
    prerequisites=["variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="z_score",
    content="z = \\frac{x - \\bar{x}}{\\sigma}",
    tier=3,
    domain="statistics",
    prerequisites=["mean", "std_dev"],
))

register_atom(Atom(
    atom_type="formula",
    name="linear_regression",
    content="m = \\frac{n\\sum xy - \\sum x \\sum y}{n\\sum x^2 - (\\sum x)^2}",
    tier=4,
    domain="statistics",
    prerequisites=["mean", "multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="correlation",
    content="r = \\frac{n\\sum xy - \\sum x \\sum y}{\\sqrt{(n\\sum x^2 - (\\sum x)^2)(n\\sum y^2 - (\\sum y)^2)}}",
    tier=4,
    domain="statistics",
    prerequisites=["std_dev", "mean"],
))

register_atom(Atom(
    atom_type="formula",
    name="hypothesis_test",
    content="t = \\frac{\\bar{x} - \\mu_0}{s / \\sqrt{n}}",
    tier=5,
    domain="statistics",
    prerequisites=["mean", "std_dev"],
))

register_atom(Atom(
    atom_type="formula",
    name="confidence_interval",
    content="CI = \\bar{x} \\pm z \\frac{\\sigma}{\\sqrt{n}}",
    tier=5,
    domain="statistics",
    prerequisites=["mean", "std_dev", "z_score"],
))

# ---------------------------------------------------------------------------
# Probability (tier 2-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="basic_prob",
    content="P(A) = \\frac{\\text{favorable}}{\\text{total}}",
    tier=2,
    domain="probability",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="conditional_prob",
    content="P(A|B) = \\frac{P(A \\cap B)}{P(B)}",
    tier=3,
    domain="probability",
    prerequisites=["basic_prob", "division"],
))

register_atom(Atom(
    atom_type="theorem",
    name="bayes_theorem",
    content="P(A|B) = \\frac{P(B|A)P(A)}{P(B)}",
    tier=4,
    domain="probability",
    prerequisites=["conditional_prob", "multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="expected_value",
    content="E[X] = \\sum_i x_i P(x_i)",
    tier=3,
    domain="probability",
    prerequisites=["multiplication", "addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="binomial_dist",
    content="P(X=k) = \\binom{n}{k} p^k (1-p)^{n-k}",
    tier=4,
    domain="probability",
    prerequisites=["binomial", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="poisson_dist",
    content="P(X=k) = \\frac{\\lambda^k e^{-\\lambda}}{k!}",
    tier=5,
    domain="probability",
    prerequisites=["exponentiation", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="variance_dist",
    content="\\text{Var}(X) = E[X^2] - (E[X])^2",
    tier=4,
    domain="probability",
    prerequisites=["expected_value", "exponentiation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="total_probability",
    content="P(A) = \\sum_i P(A|B_i) P(B_i)",
    tier=4,
    domain="probability",
    prerequisites=["conditional_prob", "addition"],
))

register_atom(Atom(
    atom_type="definition",
    name="independence_test",
    content="A \\perp B \\iff P(A \\cap B) = P(A) P(B)",
    tier=3,
    domain="probability",
    prerequisites=["basic_prob", "multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="markov_chain",
    content="\\pi_{t+1} = \\pi_t T",
    tier=5,
    domain="probability",
    prerequisites=["matrix_multiply", "expected_value"],
))

# ---------------------------------------------------------------------------
# Quantum mechanics (tier 4-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="complex_arithmetic",
    content="(a+bi)(c+di) = (ac-bd) + (ad+bc)i",
    tier=4,
    domain="quantum",
    prerequisites=["multiplication", "addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="complex_modulus",
    content="|a+bi| = \\sqrt{a^2 + b^2}",
    tier=4,
    domain="quantum",
    prerequisites=["complex_arithmetic", "exponentiation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="euler_formula",
    content="e^{i\\theta} = \\cos\\theta + i\\sin\\theta",
    tier=5,
    domain="quantum",
    prerequisites=["complex_arithmetic", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="qubit_measure",
    content="P(0) = |\\alpha|^2, \\quad P(1) = |\\beta|^2",
    tier=5,
    domain="quantum",
    prerequisites=["complex_modulus"],
))

register_atom(Atom(
    atom_type="formula",
    name="quantum_gate",
    content="|\\psi'\\rangle = U|\\psi\\rangle",
    tier=6,
    domain="quantum",
    prerequisites=["qubit_measure", "matrix_multiply"],
))

# ---------------------------------------------------------------------------
# Computer science — logic and binary (tier 3-4)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="boolean_algebra",
    content="\\overline{A \\wedge B} = \\overline{A} \\vee \\overline{B} \\text{ (De Morgan)}",
    tier=3,
    domain="computer_science",
    prerequisites=["logic"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="binary_arithmetic",
    content="\\text{binary addition with carry propagation}",
    tier=3,
    domain="computer_science",
    prerequisites=["addition", "base_conversion"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="twos_complement",
    content="\\text{invert all bits and add 1}",
    tier=4,
    domain="computer_science",
    prerequisites=["binary_arithmetic"],
))

register_atom(Atom(
    atom_type="definition",
    name="logic_gate_eval",
    content="\\text{AND, OR, NOT, NAND, NOR, XOR gate evaluation}",
    tier=3,
    domain="computer_science",
    prerequisites=["logic"],
))

# ---------------------------------------------------------------------------
# Computer science — ML and neural (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="sigmoid_eval",
    content="\\sigma(x) = \\frac{1}{1 + e^{-x}}",
    tier=4,
    domain="computer_science",
    prerequisites=["exponentiation", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="cross_entropy",
    content="H(p, q) = -\\sum_i p_i \\log q_i",
    tier=4,
    domain="computer_science",
    prerequisites=["multiplication", "addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="info_entropy",
    content="H(X) = -\\sum_i p_i \\log_2 p_i",
    tier=4,
    domain="computer_science",
    prerequisites=["multiplication", "addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="softmax_eval",
    content="\\text{softmax}(x_i) = \\frac{e^{x_i}}{\\sum_j e^{x_j}}",
    tier=5,
    domain="computer_science",
    prerequisites=["exponentiation", "division", "addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="attention_score",
    content="\\text{score} = \\frac{QK^T}{\\sqrt{d_k}}",
    tier=5,
    domain="computer_science",
    prerequisites=["matrix_multiply", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="backprop_simple",
    content="\\frac{\\partial f}{\\partial x} = 2ax + b \\text{ for } f(x) = ax^2 + bx + c",
    tier=5,
    domain="computer_science",
    prerequisites=["derivative_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="neural_forward",
    content="z = Wx + b, \\quad a = \\sigma(z)",
    tier=6,
    domain="computer_science",
    prerequisites=["matrix_multiply", "sigmoid_eval"],
))

# ---------------------------------------------------------------------------
# Computer science — algorithms (tier 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="big_o",
    content="O(g(n)): \\exists c, n_0 \\text{ s.t. } f(n) \\leq c \\cdot g(n) \\; \\forall n \\geq n_0",
    tier=4,
    domain="computer_science",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="convolution",
    content="(f * g)[n] = \\sum_{k} f[k] \\cdot g[n-k]",
    tier=5,
    domain="computer_science",
    prerequisites=["multiplication", "addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="polynomial_hash",
    content="h(s) = \\sum_{i=0}^{n-1} s_i \\cdot p^i \\mod m",
    tier=5,
    domain="computer_science",
    prerequisites=["mod_pow", "addition"],
))
