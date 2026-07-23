"""Atoms for measurement."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


register_atom(Atom(atom_type="algorithm", name="unit_conversion_length",
    content="Length conversions: 1 km = 1000 m, 1 m = 100 cm, 1 cm = 10 mm. "
    "Imperial: 1 mile = 1.609 km, 1 foot = 0.3048 m, 1 inch = 2.54 cm. "
    "Multiply by the conversion factor to change units.",
    example="5 miles to km: 5 * 1.609 = 8.045 km",
    tier=0, domain="measurement",
    source="Wikipedia contributors, 'Conversion of units', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conversion_of_units"))

register_atom(Atom(atom_type="algorithm", name="unit_conversion_mass",
    content="Mass conversions: 1 kg = 1000 g, 1 g = 1000 mg. "
    "Imperial: 1 pound = 0.4536 kg, 1 ounce = 28.35 g. "
    "1 metric ton = 1000 kg.",
    example="10 pounds to kg: 10 * 0.4536 = 4.536 kg",
    tier=0, domain="measurement",
    source="Wikipedia contributors, 'Conversion of units', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conversion_of_units"))

register_atom(Atom(atom_type="algorithm", name="unit_conversion_temp",
    content="Temperature conversions: C = (F - 32) * 5/9, F = C * 9/5 + 32, K = C + 273.15. "
    "Key points: water freezes at 0C/32F/273.15K, boils at 100C/212F/373.15K.",
    example="98.6 F to C: (98.6 - 32) * 5/9 = 37.0 C. 100 C to K: 100 + 273.15 = 373.15 K",
    tier=0, domain="measurement",
    source="Wikipedia contributors, 'Conversion of units of temperature', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conversion_of_units_of_temperature"))

register_atom(Atom(atom_type="algorithm", name="time_arithmetic",
    content="Time arithmetic: 1 hour = 60 minutes, 1 minute = 60 seconds, 1 day = 24 hours. "
    "Adding times may require carrying: 45 min + 30 min = 75 min = 1 hr 15 min. "
    "Elapsed time: end_time - start_time, borrowing from hours if needed.",
    tier=1, domain="measurement",
    source="Wikipedia contributors, 'Time', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Time"))

register_atom(Atom(atom_type="algorithm", name="significant_figures",
    content="Significant figures indicate precision. Rules: all nonzero digits are significant; "
    "zeros between nonzero digits are significant; leading zeros are not; trailing zeros after "
    "decimal point are significant. In multiplication/division, the result has as many sig figs "
    "as the input with the fewest.",
    tier=1, domain="measurement",
    source="Wikipedia contributors, 'Significant figures', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Significant_figures"))

register_atom(Atom(atom_type="algorithm", name="scientific_notation",
    content="Scientific notation writes a number as a * 10^n where 1 <= |a| < 10. "
    "Example: 6,700,000 = 6.7 * 10^6. 0.00042 = 4.2 * 10^-4. "
    "To multiply: multiply coefficients and add exponents. To divide: divide coefficients, subtract exponents.",
    tier=1, domain="measurement",
    source="Wikipedia contributors, 'Scientific notation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Scientific_notation"))
