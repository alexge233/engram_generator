"""Atoms for sequences."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


register_atom(Atom(atom_type="formula", name="arithmetic_sequence",
    content="An arithmetic sequence has constant difference d: a_n = a_1 + (n-1)*d. "
    "Sum of first n terms: S_n = n*(a_1 + a_n)/2 = n*(2*a_1 + (n-1)*d)/2.",
    example="a_1=3, d=5: a_10 = 3 + 9*5 = 48. S_10 = 10*(3+48)/2 = 255",
    tier=1, domain="sequences",
    source="Wikipedia contributors, 'Arithmetic progression', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Arithmetic_progression"))

register_atom(Atom(atom_type="formula", name="geometric_sequence",
    content="A geometric sequence has constant ratio r: a_n = a_1 * r^(n-1). "
    "Sum of first n terms: S_n = a_1 * (1 - r^n) / (1 - r) for r != 1. "
    "Infinite sum (|r| < 1): S = a_1 / (1 - r).",
    example="a_1=2, r=3: a_5 = 2*3^4 = 162. S_5 = 2*(1-3^5)/(1-3) = 2*(-242)/(-2) = 242",
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
