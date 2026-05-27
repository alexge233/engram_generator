"""Atoms for numerical."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


register_atom(Atom(atom_type="algorithm", name="bisection_method",
    content="The bisection method finds a root of f(x) = 0 in [a, b] where f(a) and f(b) have opposite signs. "
    "Compute mid = (a+b)/2. If f(mid) has the same sign as f(a), replace a; otherwise replace b. "
    "Repeat until |b-a| < tolerance. Convergence is guaranteed but slow (halves interval each step).",
    tier=3, domain="numerical",
    source="Wikipedia contributors, 'Bisection method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bisection_method"))

register_atom(Atom(atom_type="algorithm", name="euler_method_ode",
    content="Euler's method approximates the solution of dy/dx = f(x, y) with initial condition y(x0) = y0. "
    "Step: y_{n+1} = y_n + h * f(x_n, y_n), x_{n+1} = x_n + h. "
    "Accuracy improves with smaller step size h. First-order method: error is O(h).",
    tier=4, domain="numerical",
    source="Wikipedia contributors, 'Euler method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euler_method",
    prerequisites=["derivative"]))

register_atom(Atom(atom_type="algorithm", name="trapezoidal_rule",
    content="The trapezoidal rule approximates a definite integral: "
    "integral(f, a, b) ≈ (b-a)/2 * (f(a) + f(b)). "
    "For n subintervals: h = (b-a)/n, integral ≈ h/2 * (f(a) + 2*sum(f(x_i)) + f(b)).",
    tier=3, domain="numerical",
    source="Wikipedia contributors, 'Trapezoidal rule', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trapezoidal_rule",
    prerequisites=["area_rectangle"]))

register_atom(Atom(atom_type="algorithm", name="numerical_derivative",
    content="The numerical derivative approximates f'(x) using finite differences: "
    "forward: (f(x+h) - f(x)) / h. Central: (f(x+h) - f(x-h)) / (2h). "
    "Central difference is more accurate (error O(h^2) vs O(h)).",
    tier=3, domain="numerical",
    source="Wikipedia contributors, 'Numerical differentiation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Numerical_differentiation",
    prerequisites=["derivative"]))
