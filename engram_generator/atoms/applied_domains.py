"""Atoms for chemistry, economics/finance, game theory, automata, spatial, numerical."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Chemistry ───────────────────────────────────────────────────────

register_atom(Atom(atom_type="formula", name="molar_mass",
    content="Molar mass is the mass of one mole (6.022×10^23 particles) of a substance in g/mol. "
    "For molecules, add the atomic masses of all atoms: H2O = 2(1.008) + 15.999 = 18.015 g/mol.",
    tier=2, domain="chemistry",
    source="Wikipedia contributors, 'Molar mass', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Molar_mass"))

register_atom(Atom(atom_type="algorithm", name="stoichiometry",
    content="Stoichiometry uses the mole ratio from a balanced equation to convert between amounts. "
    "For 2H2 + O2 -> 2H2O: 2 mol H2 produces 2 mol H2O. "
    "Steps: balance equation, convert to moles, apply ratio, convert to desired unit.",
    tier=3, domain="chemistry",
    source="Wikipedia contributors, 'Stoichiometry', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stoichiometry",
    prerequisites=["molar_mass"]))

register_atom(Atom(atom_type="formula", name="molarity",
    content="Molarity M = moles of solute / litres of solution. "
    "To dilute: M1*V1 = M2*V2. A 0.5 M NaCl solution contains 0.5 moles of NaCl per litre.",
    tier=3, domain="chemistry",
    source="Wikipedia contributors, 'Molar concentration', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Molar_concentration",
    prerequisites=["molar_mass"]))

register_atom(Atom(atom_type="formula", name="ph_calculation",
    content="pH = -log10([H+]). Neutral pH = 7. Acidic < 7, basic > 7. "
    "pOH = -log10([OH-]). pH + pOH = 14 at 25°C. "
    "For a 0.01 M HCl solution: pH = -log10(0.01) = 2.",
    tier=3, domain="chemistry",
    source="Wikipedia contributors, 'pH', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/PH",
    prerequisites=["logarithm"]))

register_atom(Atom(atom_type="algorithm", name="balancing_equation",
    content="A balanced chemical equation has equal numbers of each type of atom on both sides. "
    "Method: (1) list elements, (2) balance most complex compound first, (3) adjust coefficients, "
    "(4) check all elements. Fe + O2 -> Fe2O3 becomes 4Fe + 3O2 -> 2Fe2O3.",
    tier=2, domain="chemistry",
    source="Wikipedia contributors, 'Chemical equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chemical_equation"))

# ── Economics / Finance ──────────────────────────────────────────────

register_atom(Atom(atom_type="formula", name="simple_interest",
    content="Simple interest: I = P * r * t, where P = principal, r = annual rate, t = time in years. "
    "Total amount: A = P + I = P(1 + rt).",
    tier=1, domain="finance",
    source="Wikipedia contributors, 'Interest', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Interest"))

register_atom(Atom(atom_type="formula", name="compound_interest",
    content="Compound interest: A = P(1 + r/n)^(nt), where n = compounding frequency per year. "
    "Continuous compounding: A = P*e^(rt). The effective annual rate = (1 + r/n)^n - 1.",
    tier=2, domain="finance",
    source="Wikipedia contributors, 'Compound interest', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Compound_interest",
    prerequisites=["simple_interest"]))

register_atom(Atom(atom_type="formula", name="present_value",
    content="Present value PV = FV / (1 + r)^t discounts a future amount to today. "
    "Net present value NPV = sum of PV of all cash flows. If NPV > 0, the investment is profitable.",
    tier=3, domain="finance",
    source="Wikipedia contributors, 'Present value', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Present_value",
    prerequisites=["compound_interest"]))

register_atom(Atom(atom_type="formula", name="roi",
    content="Return on investment: ROI = (gain - cost) / cost * 100%. "
    "A $1000 investment that returns $1200 has ROI = (1200-1000)/1000 = 20%.",
    tier=1, domain="finance",
    source="Wikipedia contributors, 'Return on investment', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Return_on_investment"))

register_atom(Atom(atom_type="formula", name="break_even",
    content="Break-even point: units = fixed_costs / (price_per_unit - variable_cost_per_unit). "
    "At break-even, total revenue equals total costs (zero profit).",
    tier=2, domain="finance",
    source="Wikipedia contributors, 'Break-even (economics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Break-even_(economics)",
    prerequisites=["division"]))

register_atom(Atom(atom_type="formula", name="depreciation",
    content="Straight-line depreciation: annual = (cost - salvage) / useful_life. "
    "Declining balance: annual = book_value * rate. "
    "Book value after t years (straight-line) = cost - t * annual_depreciation.",
    tier=2, domain="finance",
    source="Wikipedia contributors, 'Depreciation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Depreciation"))

# ── Game Theory ──────────────────────────────────────────────────────

register_atom(Atom(atom_type="definition", name="payoff_matrix",
    content="A payoff matrix shows the outcomes for each combination of strategies by players. "
    "Each cell contains payoffs (row_player, column_player). "
    "In the Prisoner's Dilemma: (C,C)=(3,3), (C,D)=(0,5), (D,C)=(5,0), (D,D)=(1,1).",
    tier=3, domain="game_theory",
    source="Wikipedia contributors, 'Normal-form game', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Normal-form_game"))

register_atom(Atom(atom_type="definition", name="dominant_strategy",
    content="A strategy dominates another if it yields a better payoff regardless of what the "
    "opponent does. A player's dominant strategy (if it exists) is the optimal choice. "
    "In Prisoner's Dilemma, 'Defect' is dominant for both players.",
    tier=3, domain="game_theory",
    source="Wikipedia contributors, 'Dominant strategy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dominant_strategy",
    prerequisites=["payoff_matrix"]))

register_atom(Atom(atom_type="definition", name="nash_equilibrium",
    content="A Nash equilibrium is a strategy profile where no player can improve their payoff "
    "by unilaterally changing strategy. In pure strategies, check each cell: if neither player "
    "benefits from deviating, it is a Nash equilibrium. A game may have zero, one, or multiple NE.",
    tier=4, domain="game_theory",
    source="Wikipedia contributors, 'Nash equilibrium', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nash_equilibrium",
    prerequisites=["dominant_strategy"]))

register_atom(Atom(atom_type="algorithm", name="minimax",
    content="Minimax strategy: maximise the minimum payoff. The maximising player picks the strategy "
    "whose worst-case outcome is highest. For zero-sum games, this is optimal. "
    "Minimax value = max over rows of (min over columns of payoff).",
    tier=4, domain="game_theory",
    source="Wikipedia contributors, 'Minimax', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Minimax",
    prerequisites=["payoff_matrix"]))

# ── Automata / Formal Languages ─────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="dfa_accept",
    content="A deterministic finite automaton (DFA) has states, a start state, accept states, "
    "and a transition function delta(state, symbol) -> state. To check if a string is accepted: "
    "start at the initial state, follow transitions for each symbol, accept if the final state "
    "is an accept state.",
    tier=3, domain="automata",
    source="Wikipedia contributors, 'Deterministic finite automaton', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Deterministic_finite_automaton"))

register_atom(Atom(atom_type="algorithm", name="nfa_simulate",
    content="A nondeterministic finite automaton (NFA) can be in multiple states simultaneously. "
    "To simulate: maintain a set of current states, for each symbol expand to all reachable states "
    "(including epsilon transitions). Accept if any final state is an accept state.",
    tier=4, domain="automata",
    source="Wikipedia contributors, 'Nondeterministic finite automaton', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton",
    prerequisites=["dfa_accept"]))

register_atom(Atom(atom_type="algorithm", name="turing_machine_step",
    content="A Turing machine has a tape, a head, states, and transition rules: "
    "(state, symbol) -> (new_state, write_symbol, move_direction). "
    "Execute one step: read symbol under head, apply the matching rule, write, move, change state.",
    tier=4, domain="automata",
    source="Wikipedia contributors, 'Turing machine', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Turing_machine",
    prerequisites=["dfa_accept"]))

# ── Spatial Reasoning ────────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="point_in_polygon",
    content="To test if a point is inside a polygon, cast a ray from the point and count crossings "
    "with polygon edges. Odd crossings = inside, even = outside. This is the ray casting algorithm.",
    tier=3, domain="spatial",
    source="Wikipedia contributors, 'Point in polygon', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Point_in_polygon",
    prerequisites=["line_intersection"]))

register_atom(Atom(atom_type="algorithm", name="convex_hull_check",
    content="A set of points is convex if, for any two points in the set, the line segment between "
    "them lies entirely within the set. The convex hull is the smallest convex set containing all points. "
    "For a polygon, check if all cross products of consecutive edge vectors have the same sign.",
    tier=4, domain="spatial",
    source="Wikipedia contributors, 'Convex hull', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convex_hull",
    prerequisites=["polygon_area"]))

register_atom(Atom(atom_type="formula", name="bounding_box",
    content="The axis-aligned bounding box (AABB) of a set of 2D points is the smallest rectangle "
    "with sides parallel to the axes that contains all points: min_x, max_x, min_y, max_y. "
    "Width = max_x - min_x, height = max_y - min_y.",
    tier=2, domain="spatial",
    source="Wikipedia contributors, 'Minimum bounding box', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Minimum_bounding_box"))

# ── Numerical Methods ────────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="bisection_method",
    content="The bisection method finds a root of f(x) = 0 in [a, b] where f(a) and f(b) have opposite signs. "
    "Compute mid = (a+b)/2. If f(mid) has the same sign as f(a), replace a; otherwise replace b. "
    "Repeat until |b-a| < tolerance. Convergence is guaranteed but slow (halves interval each step).",
    tier=3, domain="numerical",
    source="Wikipedia contributors, 'Bisection method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bisection_method"))

register_atom(Atom(atom_type="algorithm", name="trapezoidal_rule",
    content="The trapezoidal rule approximates a definite integral: "
    "integral(f, a, b) ≈ (b-a)/2 * (f(a) + f(b)). "
    "For n subintervals: h = (b-a)/n, integral ≈ h/2 * (f(a) + 2*sum(f(x_i)) + f(b)).",
    tier=3, domain="numerical",
    source="Wikipedia contributors, 'Trapezoidal rule', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trapezoidal_rule",
    prerequisites=["area_rectangle"]))

register_atom(Atom(atom_type="algorithm", name="euler_method_ode",
    content="Euler's method approximates the solution of dy/dx = f(x, y) with initial condition y(x0) = y0. "
    "Step: y_{n+1} = y_n + h * f(x_n, y_n), x_{n+1} = x_n + h. "
    "Accuracy improves with smaller step size h. First-order method: error is O(h).",
    tier=4, domain="numerical",
    source="Wikipedia contributors, 'Euler method', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euler_method",
    prerequisites=["derivative"]))

register_atom(Atom(atom_type="algorithm", name="numerical_derivative",
    content="The numerical derivative approximates f'(x) using finite differences: "
    "forward: (f(x+h) - f(x)) / h. Central: (f(x+h) - f(x-h)) / (2h). "
    "Central difference is more accurate (error O(h^2) vs O(h)).",
    tier=3, domain="numerical",
    source="Wikipedia contributors, 'Numerical differentiation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Numerical_differentiation",
    prerequisites=["derivative"]))
