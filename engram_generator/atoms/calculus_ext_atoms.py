"""Knowledge atoms for calculus_ext and calculus_deep generators.

Covers implicit/logarithmic differentiation, integration techniques,
multivariable calculus, vector calculus, and series. Each atom includes
the canonical formula from Wikipedia or Wolfram MathWorld plus a
worked example with known input/output for verification.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ===================================================================
# calculus_ext atoms (15 generators, tiers 5-6)
# ===================================================================

register_atom(Atom(
    atom_type="formula",
    name="implicit_differentiation",
    content=(
        "Implicit differentiation is used to find dy/dx when y is "
        "defined implicitly by an equation F(x,y) = 0. Differentiate "
        "both sides with respect to x, treating y as a function of x "
        "and applying the chain rule: dF/dx + (dF/dy)(dy/dx) = 0, "
        "so dy/dx = -(dF/dx)/(dF/dy). For example, given "
        "x^2 + y^2 = r^2, differentiating gives 2x + 2y(dy/dx) = 0, "
        "hence dy/dx = -x/y."
    ),
    example=(
        "Given x^2 + y^2 = 25, find dy/dx. "
        "Differentiate: 2x + 2y(dy/dx) = 0. "
        "Solve: dy/dx = -x/y. At (3,4): dy/dx = -3/4."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Implicit function', section 'Implicit differentiation'",
    source_url="https://en.wikipedia.org/wiki/Implicit_function#Implicit_differentiation",
    prerequisites=["chain_rule", "power_rule"],
))

register_atom(Atom(
    atom_type="formula",
    name="logarithmic_differentiation",
    content=(
        "Logarithmic differentiation is a technique for differentiating "
        "functions of the form y = f(x)^{g(x)} or products/quotients "
        "of many factors. Take the natural log of both sides: "
        "ln y = g(x) ln f(x), then differentiate implicitly: "
        "(1/y)(dy/dx) = g'(x) ln f(x) + g(x) f'(x)/f(x), "
        "so dy/dx = y [g'(x) ln f(x) + g(x) f'(x)/f(x)]."
    ),
    example=(
        "Given y = x^x, find dy/dx. "
        "ln y = x ln x. Differentiate: (1/y)(dy/dx) = ln x + 1. "
        "dy/dx = x^x (ln x + 1). At x=2: dy/dx = 4(ln 2 + 1) = 6.773."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Logarithmic differentiation'",
    source_url="https://en.wikipedia.org/wiki/Logarithmic_differentiation",
    prerequisites=["chain_rule", "implicit_differentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="integration_by_substitution",
    content=(
        "Integration by substitution (u-substitution) reverses the "
        "chain rule: integral of f(g(x)) g'(x) dx = integral of "
        "f(u) du, where u = g(x). For definite integrals, the limits "
        "must be changed to u-values: integral from a to b of "
        "f(g(x)) g'(x) dx = integral from g(a) to g(b) of f(u) du."
    ),
    example=(
        "Evaluate integral of 2x cos(x^2) dx. "
        "Let u = x^2, du = 2x dx. "
        "Integral becomes integral of cos(u) du = sin(u) + C = sin(x^2) + C."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Integration by substitution'",
    source_url="https://en.wikipedia.org/wiki/Integration_by_substitution",
    prerequisites=["definite_integral", "chain_rule"],
))

register_atom(Atom(
    atom_type="formula",
    name="integration_trig_sub",
    content=(
        "Trigonometric substitution replaces algebraic expressions "
        "with trigonometric ones to simplify integrals containing "
        "sqrt(a^2 - x^2), sqrt(a^2 + x^2), or sqrt(x^2 - a^2). "
        "For sqrt(a^2 - x^2): let x = a sin(theta). "
        "For sqrt(a^2 + x^2): let x = a tan(theta). "
        "For sqrt(x^2 - a^2): let x = a sec(theta)."
    ),
    example=(
        "Evaluate integral of 1/sqrt(4-x^2) dx. "
        "Let x = 2 sin(theta), dx = 2 cos(theta) d(theta). "
        "sqrt(4-x^2) = 2 cos(theta). "
        "Integral = integral of d(theta) = theta + C = arcsin(x/2) + C."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Trigonometric substitution'",
    source_url="https://en.wikipedia.org/wiki/Trigonometric_substitution",
    prerequisites=["integration_by_substitution"],
))

register_atom(Atom(
    atom_type="formula",
    name="arc_length",
    content=(
        "The arc length of a curve y = f(x) from x = a to x = b is "
        "L = integral from a to b of sqrt(1 + (dy/dx)^2) dx. "
        "For parametric curves x = x(t), y = y(t): "
        "L = integral from t1 to t2 of sqrt((dx/dt)^2 + (dy/dt)^2) dt. "
        "For polar curves r = f(theta): "
        "L = integral of sqrt(r^2 + (dr/d(theta))^2) d(theta)."
    ),
    example=(
        "Find arc length of y = x^(3/2) from x=0 to x=4. "
        "dy/dx = (3/2)x^(1/2). 1 + (dy/dx)^2 = 1 + 9x/4. "
        "L = integral from 0 to 4 of sqrt(1 + 9x/4) dx "
        "= (8/27)[(1+9x/4)^(3/2)] from 0 to 4 = (8/27)(10^(3/2) - 1) = 9.073."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Arc length'",
    source_url="https://en.wikipedia.org/wiki/Arc_length",
    prerequisites=["definite_integral", "power_rule"],
))

register_atom(Atom(
    atom_type="formula",
    name="surface_area_revolution",
    content=(
        "The surface area of a surface of revolution generated by "
        "rotating y = f(x) about the x-axis from x = a to x = b is "
        "S = 2*pi * integral from a to b of f(x) sqrt(1 + (f'(x))^2) dx. "
        "For rotation about the y-axis: "
        "S = 2*pi * integral from a to b of x sqrt(1 + (f'(x))^2) dx."
    ),
    example=(
        "Surface area of y = sqrt(x), 0 <= x <= 1, rotated about x-axis. "
        "f(x) = sqrt(x), f'(x) = 1/(2 sqrt(x)). "
        "S = 2*pi * integral of sqrt(x) * sqrt(1 + 1/(4x)) dx "
        "= pi/6 * (5*sqrt(5) - 1) = 5.330."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Surface of revolution'",
    source_url="https://en.wikipedia.org/wiki/Surface_of_revolution",
    prerequisites=["arc_length", "definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="volume_revolution",
    content=(
        "The volume of a solid of revolution formed by rotating "
        "y = f(x) about the x-axis from x=a to x=b is given by the "
        "disk method: V = pi * integral from a to b of [f(x)]^2 dx. "
        "The shell method rotates about the y-axis: "
        "V = 2*pi * integral from a to b of x * f(x) dx."
    ),
    example=(
        "Volume of y = x^2 from x=0 to x=2 rotated about x-axis. "
        "V = pi * integral from 0 to 2 of x^4 dx "
        "= pi * [x^5/5] from 0 to 2 = 32*pi/5 = 20.106."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Solid of revolution'",
    source_url="https://en.wikipedia.org/wiki/Solid_of_revolution",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="parametric_derivative",
    content=(
        "For a curve defined parametrically as x = x(t), y = y(t), "
        "the first derivative is dy/dx = (dy/dt)/(dx/dt), provided "
        "dx/dt != 0. The second derivative is "
        "d^2y/dx^2 = (d/dt)(dy/dx) / (dx/dt)."
    ),
    example=(
        "Given x = t^2, y = t^3, find dy/dx. "
        "dx/dt = 2t, dy/dt = 3t^2. "
        "dy/dx = 3t^2 / 2t = 3t/2. At t=2: dy/dx = 3."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Parametric equation', section 'Calculus with parametric curves'",
    source_url="https://en.wikipedia.org/wiki/Parametric_equation#Calculus_with_parametric_curves",
    prerequisites=["chain_rule"],
))

register_atom(Atom(
    atom_type="formula",
    name="polar_area",
    content=(
        "The area enclosed by a polar curve r = f(theta) from "
        "theta = alpha to theta = beta is "
        "A = (1/2) integral from alpha to beta of r^2 d(theta). "
        "For the area between two polar curves r1 and r2: "
        "A = (1/2) integral of (r2^2 - r1^2) d(theta)."
    ),
    example=(
        "Area enclosed by r = 2 cos(theta) (a circle of radius 1). "
        "A = (1/2) integral from 0 to pi of (2 cos theta)^2 d(theta) "
        "= 2 integral from 0 to pi of cos^2(theta) d(theta) = pi."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Polar coordinate system', section 'Integral calculus'",
    source_url="https://en.wikipedia.org/wiki/Polar_coordinate_system#Integral_calculus_(area)",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="multivariable_chain_rule",
    content=(
        "Multivariable chain rule: If z = f(x,y) where x = g(t) and "
        "y = h(t), then dz/dt = (partial f/partial x)(dx/dt) + "
        "(partial f/partial y)(dy/dt). More generally, for "
        "z = f(x1,...,xn) where each xi = xi(t1,...,tm): "
        "partial z/partial tj = sum_i (partial f/partial xi)(partial xi/partial tj)."
    ),
    example=(
        "Given z = x^2 y, x = t^2, y = t^3, find dz/dt. "
        "partial z/partial x = 2xy, partial z/partial y = x^2. "
        "dx/dt = 2t, dy/dt = 3t^2. "
        "dz/dt = 2xy(2t) + x^2(3t^2) = 2(t^2)(t^3)(2t) + (t^4)(3t^2) "
        "= 4t^6 + 3t^6 = 7t^6. At t=1: dz/dt = 7."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Chain rule', section 'Multivariable case'",
    source_url="https://en.wikipedia.org/wiki/Chain_rule#Multivariable_case",
    prerequisites=["chain_rule", "partial_derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="improper_integral",
    content=(
        "An improper integral is a definite integral with an infinite "
        "limit of integration or an integrand with a discontinuity in "
        "the interval. For infinite limits: integral from a to infinity "
        "of f(x) dx = lim(b->infinity) integral from a to b of f(x) dx. "
        "The integral converges if this limit exists and is finite."
    ),
    example=(
        "Evaluate integral from 1 to infinity of 1/x^2 dx. "
        "= lim(b->inf) [-1/x] from 1 to b = lim(b->inf) (-1/b + 1) = 1. "
        "The integral converges to 1."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Improper integral'",
    source_url="https://en.wikipedia.org/wiki/Improper_integral",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="double_integral",
    content=(
        "A double integral computes volume under a surface z = f(x,y) "
        "over a region R in the xy-plane: "
        "integral integral_R f(x,y) dA. By Fubini's theorem, if f is "
        "continuous on a rectangular region [a,b] x [c,d]: "
        "integral integral_R f dA = integral from a to b "
        "(integral from c to d f(x,y) dy) dx."
    ),
    example=(
        "Evaluate integral integral of xy dA over [0,1] x [0,2]. "
        "= integral from 0 to 1 (integral from 0 to 2 xy dy) dx "
        "= integral from 0 to 1 [xy^2/2] from 0 to 2 dx "
        "= integral from 0 to 1 of 2x dx = [x^2] from 0 to 1 = 1."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Multiple integral', section 'Double integral'",
    source_url="https://en.wikipedia.org/wiki/Multiple_integral#Double_integral",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="triple_integral",
    content=(
        "A triple integral extends the double integral to three "
        "dimensions: integral integral integral_V f(x,y,z) dV. "
        "In Cartesian coordinates: "
        "integral from a to b (integral from c(x) to d(x) "
        "(integral from e(x,y) to f(x,y) f dz) dy) dx. "
        "In cylindrical: dV = r dr d(theta) dz. "
        "In spherical: dV = rho^2 sin(phi) d(rho) d(phi) d(theta)."
    ),
    example=(
        "Volume of unit sphere using triple integral in spherical coords. "
        "V = integral from 0 to 2*pi (integral from 0 to pi "
        "(integral from 0 to 1 rho^2 sin(phi) d(rho)) d(phi)) d(theta) "
        "= (2*pi)(2)(1/3) = 4*pi/3 = 4.189."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Multiple integral', section 'Triple integral'",
    source_url="https://en.wikipedia.org/wiki/Multiple_integral#Triple_integral",
    prerequisites=["double_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="line_integral",
    content=(
        "A line integral (or path integral) of a vector field "
        "F = (P,Q) along a curve C parameterised by r(t) for "
        "a <= t <= b is: integral_C F . dr = integral from a to b of "
        "F(r(t)) . r'(t) dt = integral of P dx + Q dy. "
        "For a scalar field f: integral_C f ds = integral from a to b "
        "of f(r(t)) |r'(t)| dt."
    ),
    example=(
        "Evaluate integral_C (x dx + y dy) along y=x from (0,0) to (1,1). "
        "Parameterise: x=t, y=t, 0<=t<=1. dx=dt, dy=dt. "
        "Integral = integral from 0 to 1 (t + t) dt = integral of 2t dt = 1."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Line integral'",
    source_url="https://en.wikipedia.org/wiki/Line_integral",
    prerequisites=["definite_integral", "parametric_derivative"],
))

register_atom(Atom(
    atom_type="theorem",
    name="greens_theorem",
    content=(
        "Green's theorem relates a line integral around a simple "
        "closed curve C to a double integral over the region D "
        "bounded by C: oint_C (P dx + Q dy) = integral integral_D "
        "(partial Q/partial x - partial P/partial y) dA. "
        "This is the two-dimensional special case of Stokes' theorem."
    ),
    example=(
        "Evaluate oint_C (y dx - x dy) where C is the unit circle. "
        "P = y, Q = -x. partial Q/partial x - partial P/partial y = -1 - 1 = -2. "
        "Integral = -2 * area(D) = -2 * pi."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Green's theorem'",
    source_url="https://en.wikipedia.org/wiki/Green%27s_theorem",
    prerequisites=["line_integral", "double_integral"],
))


# ===================================================================
# calculus_deep atoms (12 generators, tiers 5-6)
# ===================================================================

register_atom(Atom(
    atom_type="theorem",
    name="stokes_theorem",
    content=(
        "Stokes' theorem (generalised): The integral of a differential "
        "form omega over the boundary of an oriented manifold M equals "
        "the integral of its exterior derivative d(omega) over M: "
        "integral_(partial M) omega = integral_M d(omega). "
        "In the classical 3D vector form: "
        "oint_C F . dr = integral integral_S (curl F) . dS, "
        "where C is the boundary of surface S."
    ),
    example=(
        "Verify Stokes' theorem for F = (y, -x, 0) on the hemisphere "
        "z = sqrt(1-x^2-y^2). curl F = (0, 0, -2). "
        "Surface integral = integral integral (-2) dA = -2*pi. "
        "Line integral around unit circle: oint (y dx - x dy) = -2*pi. Both match."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Stokes' theorem'",
    source_url="https://en.wikipedia.org/wiki/Stokes%27_theorem",
    prerequisites=["line_integral", "curl_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="divergence_theorem",
    content=(
        "The divergence theorem (Gauss's theorem) states that the "
        "outward flux of a vector field F through a closed surface S "
        "equals the volume integral of the divergence of F over the "
        "region V enclosed by S: "
        "oiint_S F . dS = integral integral integral_V (div F) dV. "
        "div F = partial F_x/partial x + partial F_y/partial y + partial F_z/partial z."
    ),
    example=(
        "F = (x, y, z). div F = 1+1+1 = 3. Over unit sphere: "
        "oiint F.dS = integral integral integral 3 dV = 3 * (4*pi/3) = 4*pi."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Divergence theorem'",
    source_url="https://en.wikipedia.org/wiki/Divergence_theorem",
    prerequisites=["triple_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="curl_compute",
    content=(
        "The curl of a vector field F = (F_x, F_y, F_z) is: "
        "curl F = nabla x F = "
        "(partial F_z/partial y - partial F_y/partial z, "
        " partial F_x/partial z - partial F_z/partial x, "
        " partial F_y/partial x - partial F_x/partial y). "
        "The curl measures the infinitesimal rotation of the field."
    ),
    example=(
        "F = (y, -x, 0). "
        "curl F = (0-0, 0-0, -1-1) = (0, 0, -2). "
        "The field has constant rotation about the z-axis."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Curl (mathematics)'",
    source_url="https://en.wikipedia.org/wiki/Curl_(mathematics)",
    prerequisites=["partial_derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="laplacian",
    content=(
        "The Laplacian of a scalar field f is the divergence of its "
        "gradient: nabla^2 f = div(grad f) = "
        "partial^2 f/partial x^2 + partial^2 f/partial y^2 + "
        "partial^2 f/partial z^2. "
        "A function with nabla^2 f = 0 is called harmonic."
    ),
    example=(
        "f(x,y,z) = x^2 + y^2 - 2z^2. "
        "partial^2 f/partial x^2 = 2, partial^2 f/partial y^2 = 2, "
        "partial^2 f/partial z^2 = -4. nabla^2 f = 2+2-4 = 0. "
        "The function is harmonic."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Laplace operator'",
    source_url="https://en.wikipedia.org/wiki/Laplace_operator",
    prerequisites=["partial_derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="jacobian_matrix",
    content=(
        "The Jacobian matrix of a vector-valued function "
        "F: R^n -> R^m is the m x n matrix of first partial "
        "derivatives: J_ij = partial F_i / partial x_j. "
        "The Jacobian determinant |J| appears in change-of-variable "
        "formulas for multiple integrals."
    ),
    example=(
        "F(r,theta) = (r cos(theta), r sin(theta)). "
        "J = [[cos(theta), -r sin(theta)], [sin(theta), r cos(theta)]]. "
        "|J| = r cos^2(theta) + r sin^2(theta) = r. "
        "This gives dA = r dr d(theta) in polar coordinates."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Jacobian matrix and determinant'",
    source_url="https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant",
    prerequisites=["partial_derivative", "determinant"],
))

register_atom(Atom(
    atom_type="formula",
    name="directional_derivative",
    content=(
        "The directional derivative of f at point p in direction u "
        "(a unit vector) is: D_u f(p) = nabla f(p) . u = "
        "sum_i (partial f/partial x_i) u_i. "
        "It gives the rate of change of f in the direction u. "
        "The maximum directional derivative is |nabla f(p)| in the "
        "direction of the gradient."
    ),
    example=(
        "f(x,y) = x^2 + 3xy, find D_u f at (1,2) in direction u = (3/5, 4/5). "
        "nabla f = (2x + 3y, 3x) = (8, 3) at (1,2). "
        "D_u f = 8*(3/5) + 3*(4/5) = 24/5 + 12/5 = 36/5 = 7.2."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Directional derivative'",
    source_url="https://en.wikipedia.org/wiki/Directional_derivative",
    prerequisites=["gradient", "partial_derivative"],
))

register_atom(Atom(
    atom_type="theorem",
    name="implicit_function",
    content=(
        "The implicit function theorem states that if F(x,y) is "
        "continuously differentiable near (a,b) with F(a,b) = 0 and "
        "partial F/partial y (a,b) != 0, then there exists a "
        "function y = g(x) defined near x = a such that "
        "F(x, g(x)) = 0, and g'(x) = -(partial F/partial x) / "
        "(partial F/partial y)."
    ),
    example=(
        "F(x,y) = x^2 + y^2 - 1 = 0 near (0,1). "
        "partial F/partial y = 2y = 2 != 0 at (0,1). "
        "So y = sqrt(1 - x^2) locally, and "
        "dy/dx = -2x/(2y) = -x/y. At (0,1): dy/dx = 0."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Implicit function theorem'",
    source_url="https://en.wikipedia.org/wiki/Implicit_function_theorem",
    prerequisites=["implicit_differentiation", "partial_derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="integration_by_parts_definite",
    content=(
        "Integration by parts for definite integrals: "
        "integral from a to b of u dv = [uv] from a to b - "
        "integral from a to b of v du. "
        "Choose u and dv using LIATE priority: Logarithmic, Inverse "
        "trig, Algebraic, Trigonometric, Exponential."
    ),
    example=(
        "Evaluate integral from 0 to 1 of x e^x dx. "
        "u = x, dv = e^x dx. du = dx, v = e^x. "
        "= [x e^x] from 0 to 1 - integral from 0 to 1 of e^x dx "
        "= (e - 0) - (e - 1) = 1."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Integration by parts'",
    source_url="https://en.wikipedia.org/wiki/Integration_by_parts",
    prerequisites=["definite_integral", "product_rule"],
))

register_atom(Atom(
    atom_type="formula",
    name="partial_fraction_integration",
    content=(
        "Partial fraction decomposition expresses a rational function "
        "P(x)/Q(x) as a sum of simpler fractions. For distinct linear "
        "factors: P(x)/((x-a)(x-b)) = A/(x-a) + B/(x-b). "
        "Each term can then be integrated as A ln|x-a|. "
        "For repeated factors (x-a)^n, include terms A_k/(x-a)^k "
        "for k = 1,...,n."
    ),
    example=(
        "Integral of 1/((x-1)(x+1)) dx. "
        "Decompose: 1/((x-1)(x+1)) = (1/2)/(x-1) - (1/2)/(x+1). "
        "Integral = (1/2) ln|x-1| - (1/2) ln|x+1| + C "
        "= (1/2) ln|(x-1)/(x+1)| + C."
    ),
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Partial fraction decomposition'",
    source_url="https://en.wikipedia.org/wiki/Partial_fraction_decomposition",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="change_of_variables",
    content=(
        "Change of variables in multiple integrals: Given a "
        "transformation T: (u,v) -> (x,y), the double integral "
        "transforms as: integral integral_R f(x,y) dx dy = "
        "integral integral_S f(T(u,v)) |det(J)| du dv, "
        "where J is the Jacobian matrix of T. "
        "Common examples: polar (|J| = r), cylindrical (|J| = r), "
        "spherical (|J| = rho^2 sin(phi))."
    ),
    example=(
        "Evaluate integral integral of e^(-(x^2+y^2)) dA over R^2. "
        "Switch to polar: x = r cos(theta), y = r sin(theta), |J| = r. "
        "= integral from 0 to 2*pi integral from 0 to inf of r e^(-r^2) dr d(theta) "
        "= 2*pi * (1/2) = pi."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Integration by substitution', section 'Substitution for multiple variables'",
    source_url="https://en.wikipedia.org/wiki/Integration_by_substitution#Substitution_for_multiple_variables",
    prerequisites=["jacobian_matrix", "double_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="contour_integral_real",
    content=(
        "Many real integrals can be evaluated by contour integration "
        "in the complex plane. The residue theorem states: "
        "oint_C f(z) dz = 2*pi*i * sum of Res(f, z_k), where z_k are "
        "poles inside C. Common technique: extend a real integral to a "
        "closed contour in C, compute residues, extract the real part."
    ),
    example=(
        "Evaluate integral from 0 to inf of 1/(1+x^2) dx. "
        "f(z) = 1/(1+z^2) has poles at z=i and z=-i. "
        "Close in upper half-plane, only z=i inside. "
        "Res(f, i) = 1/(2i). Result = 2*pi*i * 1/(2i) = pi. "
        "Integral from 0 to inf = pi/2."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Residue theorem'",
    source_url="https://en.wikipedia.org/wiki/Residue_theorem",
    prerequisites=["residue_compute", "contour_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="surface_integral",
    content=(
        "The surface integral of a scalar field f over a surface S "
        "parameterised by r(u,v) is: "
        "integral integral_S f dS = integral integral_D f(r(u,v)) "
        "|partial r/partial u x partial r/partial v| du dv. "
        "For a vector field F: "
        "integral integral_S F . dS = integral integral_D F . "
        "(partial r/partial u x partial r/partial v) du dv."
    ),
    example=(
        "Surface integral of f=1 over sphere of radius R (surface area). "
        "Parameterise: r(phi,theta) = (R sin(phi) cos(theta), R sin(phi) sin(theta), R cos(phi)). "
        "|r_phi x r_theta| = R^2 sin(phi). "
        "S = integral from 0 to 2*pi integral from 0 to pi R^2 sin(phi) d(phi) d(theta) = 4*pi*R^2."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Surface integral'",
    source_url="https://en.wikipedia.org/wiki/Surface_integral",
    prerequisites=["double_integral", "cross_product"],
))

register_atom(Atom(
    atom_type="formula",
    name="vector_potential",
    content=(
        "A vector potential A for a solenoidal vector field B (div B = 0) "
        "satisfies curl A = B. The vector potential is not unique: "
        "A' = A + grad(f) gives the same B for any scalar f (gauge freedom). "
        "In electromagnetism, B = curl A relates the magnetic field to "
        "its vector potential."
    ),
    example=(
        "Find vector potential A for B = (0, 0, B_0) (uniform field). "
        "A = (1/2) B x r = (1/2)(B_0)(-y, x, 0) = (-B_0 y/2, B_0 x/2, 0). "
        "Verify: curl A = (0, 0, B_0/2 + B_0/2) = (0, 0, B_0). Correct."
    ),
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Vector potential'",
    source_url="https://en.wikipedia.org/wiki/Vector_potential",
    prerequisites=["curl_compute"],
))
