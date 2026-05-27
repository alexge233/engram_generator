"""Atoms for trigonometry, measurement/units, and sequences/series."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Trigonometry ────────────────────────────────────────────────────

register_atom(Atom(atom_type="formula", name="sin_cos_eval",
    content="Sine and cosine evaluate the y and x coordinates on the unit circle at angle theta. "
    "Key values: sin(0)=0, sin(30)=0.5, sin(45)=sqrt(2)/2, sin(60)=sqrt(3)/2, sin(90)=1. "
    "cos(theta) = sin(90 - theta). sin^2(theta) + cos^2(theta) = 1.",
    tier=1, domain="trigonometry",
    source="Wikipedia contributors, 'Trigonometric functions', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trigonometric_functions"))

register_atom(Atom(atom_type="formula", name="tan_eval",
    content="Tangent is defined as tan(theta) = sin(theta) / cos(theta). "
    "tan(0)=0, tan(45)=1, tan(60)=sqrt(3). Undefined at 90, 270 degrees (cos=0). "
    "The period of tangent is 180 degrees (pi radians).",
    tier=1, domain="trigonometry",
    source="Wikipedia contributors, 'Trigonometric functions', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Trigonometric_functions",
    prerequisites=["sin_cos_eval"]))

register_atom(Atom(atom_type="formula", name="angle_conversion",
    content="To convert degrees to radians: rad = deg * pi / 180. "
    "To convert radians to degrees: deg = rad * 180 / pi. "
    "Key conversions: 180 deg = pi rad, 90 deg = pi/2, 360 deg = 2*pi.",
    tier=1, domain="trigonometry",
    source="Wikipedia contributors, 'Radian', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Radian"))

register_atom(Atom(atom_type="theorem", name="law_of_sines",
    content="In any triangle: a/sin(A) = b/sin(B) = c/sin(C) = 2R, "
    "where a,b,c are sides opposite angles A,B,C and R is the circumradius. "
    "Used to solve triangles when given two angles and one side (AAS/ASA).",
    tier=2, domain="trigonometry",
    source="Wikipedia contributors, 'Law of sines', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Law_of_sines",
    prerequisites=["sin_cos_eval", "angle_sum_triangle"]))

register_atom(Atom(atom_type="theorem", name="law_of_cosines",
    content="In any triangle: c^2 = a^2 + b^2 - 2ab*cos(C). Generalises the Pythagorean "
    "theorem (when C=90, cos(C)=0). Used to find a side given two sides and the included angle (SAS), "
    "or to find an angle given three sides (SSS).",
    tier=2, domain="trigonometry",
    source="Wikipedia contributors, 'Law of cosines', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Law_of_cosines",
    prerequisites=["sin_cos_eval", "pythagorean"]))

register_atom(Atom(atom_type="identity", name="trig_identity",
    content="Fundamental identities: sin^2+cos^2=1, 1+tan^2=sec^2, 1+cot^2=csc^2. "
    "Double angle: sin(2x)=2sin(x)cos(x), cos(2x)=cos^2(x)-sin^2(x). "
    "Sum: sin(a+b)=sin(a)cos(b)+cos(a)sin(b).",
    tier=3, domain="trigonometry",
    source="Wikipedia contributors, 'List of trigonometric identities', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/List_of_trigonometric_identities",
    prerequisites=["sin_cos_eval", "tan_eval"]))

# ── Measurement / Units ─────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="unit_conversion_length",
    content="Length conversions: 1 km = 1000 m, 1 m = 100 cm, 1 cm = 10 mm. "
    "Imperial: 1 mile = 1.609 km, 1 foot = 0.3048 m, 1 inch = 2.54 cm. "
    "Multiply by the conversion factor to change units.",
    tier=0, domain="measurement",
    source="Wikipedia contributors, 'Conversion of units', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conversion_of_units"))

register_atom(Atom(atom_type="algorithm", name="unit_conversion_mass",
    content="Mass conversions: 1 kg = 1000 g, 1 g = 1000 mg. "
    "Imperial: 1 pound = 0.4536 kg, 1 ounce = 28.35 g. "
    "1 metric ton = 1000 kg.",
    tier=0, domain="measurement",
    source="Wikipedia contributors, 'Conversion of units', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conversion_of_units"))

register_atom(Atom(atom_type="algorithm", name="unit_conversion_temp",
    content="Temperature conversions: C = (F - 32) * 5/9, F = C * 9/5 + 32, K = C + 273.15. "
    "Key points: water freezes at 0C/32F/273.15K, boils at 100C/212F/373.15K.",
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

# ── Sequences & Series ──────────────────────────────────────────────

register_atom(Atom(atom_type="formula", name="arithmetic_sequence",
    content="An arithmetic sequence has constant difference d: a_n = a_1 + (n-1)*d. "
    "Sum of first n terms: S_n = n*(a_1 + a_n)/2 = n*(2*a_1 + (n-1)*d)/2.",
    tier=1, domain="sequences",
    source="Wikipedia contributors, 'Arithmetic progression', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Arithmetic_progression"))

register_atom(Atom(atom_type="formula", name="geometric_sequence",
    content="A geometric sequence has constant ratio r: a_n = a_1 * r^(n-1). "
    "Sum of first n terms: S_n = a_1 * (1 - r^n) / (1 - r) for r != 1. "
    "Infinite sum (|r| < 1): S = a_1 / (1 - r).",
    tier=1, domain="sequences",
    source="Wikipedia contributors, 'Geometric progression', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Geometric_progression"))

register_atom(Atom(atom_type="formula", name="sequence_sum",
    content="Sum of first n natural numbers: n*(n+1)/2. Sum of squares: n*(n+1)*(2n+1)/6. "
    "Sum of cubes: [n*(n+1)/2]^2. These are closed-form formulas for common series.",
    tier=2, domain="sequences",
    source="Wikipedia contributors, 'Summation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Summation",
    prerequisites=["arithmetic_sequence"]))

register_atom(Atom(atom_type="definition", name="convergent_series",
    content="An infinite series converges if its partial sums approach a finite limit. "
    "Geometric series with |r|<1 converges to a/(1-r). The harmonic series 1+1/2+1/3+... diverges. "
    "Tests: ratio test, comparison test, integral test.",
    tier=3, domain="sequences",
    source="Wikipedia contributors, 'Convergent series', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convergent_series",
    prerequisites=["geometric_sequence"]))

# ── Combinatorics ────────────────────────────────────────────────────

register_atom(Atom(atom_type="formula", name="combination_count",
    content="C(n,k) = n! / (k! * (n-k)!) counts the number of ways to choose k items from n "
    "without regard to order. Also written as 'n choose k'. C(5,2) = 10.",
    tier=2, domain="combinatorics",
    source="Wikipedia contributors, 'Combination', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Combination"))

register_atom(Atom(atom_type="formula", name="permutation_with_rep",
    content="Permutations with repetition: n^k arrangements when choosing k items from n with replacement. "
    "Without repetition: P(n,k) = n! / (n-k)!. Multiset permutations of n items with groups of "
    "sizes n1,n2,...: n! / (n1! * n2! * ...).",
    tier=2, domain="combinatorics",
    source="Wikipedia contributors, 'Permutation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Permutation"))

register_atom(Atom(atom_type="theorem", name="pigeonhole",
    content="The pigeonhole principle: if n items are put into m containers with n > m, then at "
    "least one container holds more than one item. Generalised: at least one container holds "
    "ceil(n/m) items. Used to prove existence results.",
    tier=2, domain="combinatorics",
    source="Wikipedia contributors, 'Pigeonhole principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pigeonhole_principle"))

register_atom(Atom(atom_type="formula", name="inclusion_exclusion",
    content="Inclusion-exclusion counts the union of overlapping sets: "
    "|A1 ∪ ... ∪ An| = sum|Ai| - sum|Ai ∩ Aj| + sum|Ai ∩ Aj ∩ Ak| - ... "
    "For derangements: D(n) = n! * sum_{k=0}^{n} (-1)^k / k!.",
    tier=3, domain="combinatorics",
    source="Wikipedia contributors, 'Inclusion-exclusion principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle",
    prerequisites=["combination_count", "venn_diagram_count"]))

register_atom(Atom(atom_type="formula", name="stars_and_bars",
    content="Stars and bars: the number of ways to distribute n identical objects into k "
    "distinct bins is C(n+k-1, k-1). Example: distributing 5 candies among 3 children "
    "gives C(7,2) = 21 ways.",
    tier=3, domain="combinatorics",
    source="Wikipedia contributors, 'Stars and bars (combinatorics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)",
    prerequisites=["combination_count"]))
