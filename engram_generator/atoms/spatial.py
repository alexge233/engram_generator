"""Atoms for spatial."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


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
