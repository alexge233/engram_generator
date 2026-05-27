"""Atoms for trigonometry."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


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
