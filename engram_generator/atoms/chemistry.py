"""Atoms for chemistry."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


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
    example="5g NaCl (MW=58.44) in 0.5L: moles = 5/58.44 = 0.0855. M = 0.0855/0.5 = 0.171 mol/L",
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
