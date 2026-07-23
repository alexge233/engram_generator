"""Atoms for economics."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


register_atom(Atom(atom_type="formula", name="simple_interest",
    content="Simple interest: I = P * r * t, where P = principal, r = annual rate, t = time in years. "
    "Total amount: A = P + I = P(1 + rt).",
    example="P=$1000, r=5%, t=3 years: I = 1000*0.05*3 = $150. A = $1150",
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
    example="FV=$1000, r=5%, t=3 years: PV = 1000/(1.05)^3 = 1000/1.1576 = $863.84",
    tier=3, domain="finance",
    source="Wikipedia contributors, 'Present value', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Present_value",
    prerequisites=["compound_interest"]))

register_atom(Atom(atom_type="formula", name="roi",
    content="Return on investment: ROI = (gain - cost) / cost * 100%. "
    "A $1000 investment that returns $1200 has ROI = (1200-1000)/1000 = 20%.",
    example="Investment=$5000, return=$6500: ROI = (6500-5000)/5000 * 100 = 30%",
    tier=1, domain="finance",
    source="Wikipedia contributors, 'Return on investment', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Return_on_investment"))

register_atom(Atom(atom_type="formula", name="break_even",
    content="Break-even point: units = fixed_costs / (price_per_unit - variable_cost_per_unit). "
    "At break-even, total revenue equals total costs (zero profit).",
    example="Fixed costs=$10000, price=$25, variable cost=$15: BEP = 10000/(25-15) = 1000 units",
    tier=2, domain="finance",
    source="Wikipedia contributors, 'Break-even (economics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Break-even_(economics)",
    prerequisites=["division"]))

register_atom(Atom(atom_type="formula", name="depreciation",
    content="Straight-line depreciation: annual = (cost - salvage) / useful_life. "
    "Declining balance: annual = book_value * rate. "
    "Book value after t years (straight-line) = cost - t * annual_depreciation.",
    example="Cost=$50000, salvage=$5000, life=10 years. Annual = (50000-5000)/10 = $4500",
    tier=2, domain="finance",
    source="Wikipedia contributors, 'Depreciation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Depreciation"))
