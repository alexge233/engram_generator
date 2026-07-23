"""Knowledge atoms for geometry — definitions, theorems, and formulas."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ── Tier 0 ─────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="area_rectangle",
    content=(
        "The area of a rectangle is computed as the product of its length "
        "and width: A = l * w. Area measures the amount of two-dimensional "
        "space enclosed within the boundary. For a rectangle with length 5 "
        "and width 3, the area is 5 * 3 = 15 square units."
    ),
    tier=0, domain="geometry",
    source="Wikipedia contributors, 'Rectangle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rectangle",
))

register_atom(Atom(
    atom_type="formula",
    name="perimeter_rectangle",
    content=(
        "The perimeter of a rectangle is the total length of its boundary: "
        "P = 2(l + w), where l is the length and w is the width. "
        "Equivalently, the perimeter is the sum of all four sides. "
        "For a rectangle with length 7 and width 4, P = 2(7 + 4) = 22."
    ),
    tier=0, domain="geometry",
    source="Wikipedia contributors, 'Perimeter', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Perimeter",
))

register_atom(Atom(
    atom_type="theorem",
    name="pythagorean",
    content=(
        "In a right-angled triangle, the square of the hypotenuse (the side "
        "opposite the right angle) is equal to the sum of the squares of the "
        "other two sides: a^2 + b^2 = c^2. This is the Pythagorean theorem. "
        "It can be used to find any side given the other two. For example, "
        "if a = 3 and b = 4, then c = sqrt(9 + 16) = sqrt(25) = 5. "
        "Common Pythagorean triples include (3, 4, 5), (5, 12, 13), "
        "(8, 15, 17), and (7, 24, 25)."
    ),
    tier=0, domain="geometry",
    source="Wikipedia contributors, 'Pythagorean theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pythagorean_theorem",
    prerequisites=["addition", "multiplication"],
))

# ── Tier 1 ─────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="area_triangle",
    content=(
        "The area of a triangle with base b and height h is A = (1/2) * b * h. "
        "The height is the perpendicular distance from the base to the opposite "
        "vertex. For a triangle with base 6 and height 4, A = 0.5 * 6 * 4 = 12. "
        "Alternative formulas include Heron's formula: A = sqrt(s(s-a)(s-b)(s-c)) "
        "where s = (a + b + c) / 2 is the semi-perimeter."
    ),
    tier=1, domain="geometry",
    source="Wikipedia contributors, 'Triangle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Triangle",
    prerequisites=["area_rectangle"],
))

register_atom(Atom(
    atom_type="formula",
    name="area_circle",
    content=(
        "The area of a circle with radius r is A = pi * r^2. The constant pi "
        "(approximately 3.14159) is the ratio of a circle's circumference to "
        "its diameter. For a circle with radius 5, A = pi * 25 ≈ 78.54."
    ),
    tier=1, domain="geometry",
    source="Wikipedia contributors, 'Area of a circle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Area_of_a_circle",
))

register_atom(Atom(
    atom_type="formula",
    name="circumference",
    content=(
        "The circumference of a circle is the distance around its boundary: "
        "C = 2 * pi * r, or equivalently C = pi * d, where d is the diameter. "
        "For a circle with radius 7, C = 2 * pi * 7 ≈ 43.98."
    ),
    tier=1, domain="geometry",
    source="Wikipedia contributors, 'Circumference', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Circumference",
))

register_atom(Atom(
    atom_type="formula",
    name="volume_box",
    content=(
        "The volume of a rectangular box (cuboid) is V = l * w * h, where l "
        "is the length, w is the width, and h is the height. Volume measures "
        "the three-dimensional space enclosed. For a box with dimensions "
        "3 x 4 x 5, V = 60 cubic units."
    ),
    example="l=5, w=3, h=4: V = 5*3*4 = 60 cubic units",
    tier=1, domain="geometry",
    source="Wikipedia contributors, 'Cuboid', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cuboid",
    prerequisites=["area_rectangle"],
))

# ── Tier 2 ─────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="distance_2d",
    content=(
        "The distance between two points (x1, y1) and (x2, y2) in the "
        "Cartesian plane is d = sqrt((x2 - x1)^2 + (y2 - y1)^2). This "
        "follows directly from the Pythagorean theorem applied to the "
        "right triangle formed by the horizontal and vertical displacements."
    ),
    tier=2, domain="geometry",
    source="Wikipedia contributors, 'Euclidean distance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euclidean_distance",
    prerequisites=["pythagorean"],
))

register_atom(Atom(
    atom_type="formula",
    name="midpoint",
    content=(
        "The midpoint of a line segment with endpoints (x1, y1) and (x2, y2) "
        "is M = ((x1 + x2) / 2, (y1 + y2) / 2). The midpoint divides the "
        "segment into two equal parts."
    ),
    example="A=(2,4), B=(6,8): M = ((2+6)/2, (4+8)/2) = (4, 6)",
    tier=2, domain="geometry",
    source="Wikipedia contributors, 'Midpoint', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Midpoint",
))

register_atom(Atom(
    atom_type="formula",
    name="slope",
    content=(
        "The slope of a line through points (x1, y1) and (x2, y2) is "
        "m = (y2 - y1) / (x2 - x1). Slope measures the steepness and "
        "direction of the line. A positive slope rises left to right, "
        "a negative slope falls, zero is horizontal, and undefined (division "
        "by zero) is vertical."
    ),
    example="A=(1,2), B=(4,8): m = (8-2)/(4-1) = 6/3 = 2",
    tier=2, domain="geometry",
    source="Wikipedia contributors, 'Slope', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Slope",
))

register_atom(Atom(
    atom_type="theorem",
    name="angle_sum_triangle",
    content=(
        "The sum of the interior angles of any triangle is exactly 180 degrees "
        "(pi radians). If two angles of a triangle are known, the third can be "
        "found by subtracting their sum from 180. This is a consequence of the "
        "parallel postulate in Euclidean geometry."
    ),
    example="Angles 50 and 60 degrees. Third angle = 180 - 50 - 60 = 70 degrees",
    tier=2, domain="geometry",
    source="Wikipedia contributors, 'Triangle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Triangle",
))

register_atom(Atom(
    atom_type="theorem",
    name="similar_triangles",
    content=(
        "Two triangles are similar if their corresponding angles are equal "
        "and their corresponding sides are proportional. If triangle ABC is "
        "similar to triangle DEF with scale factor k, then DE = k * AB, "
        "EF = k * BC, and DF = k * AC. The AA (angle-angle) criterion states "
        "that two triangles are similar if two pairs of corresponding angles "
        "are equal."
    ),
    example="Triangle 1: sides 3,4,5. Triangle 2 scale factor 2: sides 6,8,10. Side ratio = 6/3 = 2",
    tier=2, domain="geometry",
    source="Wikipedia contributors, 'Similarity (geometry)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Similarity_(geometry)",
    prerequisites=["angle_sum_triangle"],
))

# ── Tier 3 ─────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="line_intersection",
    content=(
        "Two lines y = m1*x + b1 and y = m2*x + b2 intersect where "
        "m1*x + b1 = m2*x + b2, giving x = (b2 - b1) / (m1 - m2). "
        "If m1 = m2, the lines are parallel and do not intersect "
        "(unless b1 = b2, in which case they are identical). The "
        "y-coordinate is found by substituting x back into either equation."
    ),
    tier=3, domain="geometry",
    source="Wikipedia contributors, 'Line-line intersection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection",
    prerequisites=["slope", "linear_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="polygon_area",
    content=(
        "The area of a simple polygon with vertices (x1,y1), ..., (xn,yn) "
        "listed in order is given by the shoelace formula: "
        "A = (1/2) |sum_{i=1}^{n} (x_i * y_{i+1} - x_{i+1} * y_i)|, "
        "where indices wrap around so that (x_{n+1}, y_{n+1}) = (x_1, y_1). "
        "The name comes from the crisscross pattern of multiplications."
    ),
    tier=3, domain="geometry",
    source="Wikipedia contributors, 'Shoelace formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shoelace_formula",
))

register_atom(Atom(
    atom_type="formula",
    name="circle_arc_length",
    content=(
        "The arc length of a circular sector with radius r and central "
        "angle theta (in radians) is s = r * theta. If the angle is in "
        "degrees, convert first: theta_rad = theta_deg * pi / 180. "
        "The full circumference corresponds to theta = 2*pi."
    ),
    example="r=5, theta=pi/3 (60 degrees): s = 5 * pi/3 = 5.236 cm",
    tier=3, domain="geometry",
    source="Wikipedia contributors, 'Arc length', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Arc_length",
    prerequisites=["circumference"],
))

register_atom(Atom(
    atom_type="formula",
    name="sector_area",
    content=(
        "The area of a circular sector with radius r and central angle "
        "theta (in radians) is A = (1/2) * r^2 * theta. This is the "
        "fraction theta / (2*pi) of the full circle area pi*r^2. "
        "For a 90-degree sector (pi/2 radians) of radius 4: "
        "A = 0.5 * 16 * (pi/2) = 4*pi ≈ 12.57."
    ),
    example="r=6, theta=pi/4 (45 degrees): A = (1/2)*36*(pi/4) = 14.137 sq units",
    tier=3, domain="geometry",
    source="Wikipedia contributors, 'Circular sector', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Circular_sector",
    prerequisites=["area_circle", "circle_arc_length"],
))

# ── Tier 4 ─────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="coordinate_rotation",
    content=(
        "To rotate a point (x, y) by angle theta counterclockwise about "
        "the origin, the new coordinates are: x' = x*cos(theta) - y*sin(theta), "
        "y' = x*sin(theta) + y*cos(theta). This is equivalent to multiplying "
        "the column vector [x, y] by the rotation matrix "
        "[[cos(theta), -sin(theta)], [sin(theta), cos(theta)]]."
    ),
    tier=4, domain="geometry",
    source="Wikipedia contributors, 'Rotation matrix', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rotation_matrix",
    prerequisites=["distance_2d"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="reflection_2d",
    content=(
        "Reflection of a point across common axes: across the x-axis, "
        "(x, y) becomes (x, -y); across the y-axis, (x, y) becomes (-x, y); "
        "across y = x, (x, y) becomes (y, x). Reflection across an arbitrary "
        "line y = mx + b requires projecting the point onto the line and "
        "computing the mirror point."
    ),
    tier=4, domain="geometry",
    source="Wikipedia contributors, 'Reflection (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Reflection_(mathematics)",
))

register_atom(Atom(
    atom_type="formula",
    name="volume_sphere",
    content=(
        "The volume of a sphere with radius r is V = (4/3) * pi * r^3. "
        "The surface area is A = 4 * pi * r^2. For a sphere of radius 3, "
        "V = (4/3) * pi * 27 = 36*pi ≈ 113.10."
    ),
    example="r=4: V = (4/3)*pi*64 = 268.08 cubic units",
    tier=4, domain="geometry",
    source="Wikipedia contributors, 'Sphere', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Sphere",
    prerequisites=["area_circle", "volume_box"],
))

register_atom(Atom(
    atom_type="formula",
    name="volume_cylinder",
    content=(
        "The volume of a cylinder with radius r and height h is "
        "V = pi * r^2 * h. The lateral surface area is 2 * pi * r * h, "
        "and the total surface area is 2 * pi * r * (r + h). "
        "For a cylinder of radius 3 and height 10, V = pi * 9 * 10 = 90*pi ≈ 282.74."
    ),
    example="r=3, h=7: V = pi*9*7 = 197.92 cubic units",
    tier=4, domain="geometry",
    source="Wikipedia contributors, 'Cylinder', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cylinder",
    prerequisites=["area_circle", "volume_box"],
))
