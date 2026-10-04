# cell: front_badge
# Front button badge with a flat rear face and enlarged rounded center button.
from build123d import *

outer_diameter = param("front_badge_outer_diameter", 15.4285714286)
outer_height = param("front_badge_outer_height", 2.0)
outer_edge_radius = param("front_badge_outer_edge_radius", 0.62)
center_diameter = param("front_badge_center_diameter", 10.5)
center_extra_height = param("front_badge_center_extra_height", 1.0)
center_edge_radius = param("front_badge_center_edge_radius", 0.24)

assert outer_diameter > 0
assert outer_height > 0
assert outer_edge_radius > 0
assert outer_edge_radius < outer_height / 2
assert center_diameter > 0
assert center_extra_height > 0
assert center_edge_radius > 0
assert center_edge_radius < center_extra_height / 2
assert center_diameter < outer_diameter

# The badge axis points toward the front (-Y). Only the front circular rim
# is rounded; the rear rim remains a planar face against the box.
outer_raw = Rot(X=90) * Cylinder(
    outer_diameter / 2,
    outer_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
outer_round_edge = outer_raw.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Y)[0]
outer_badge = fillet(outer_round_edge, outer_edge_radius)

center_raw = Pos(0, -outer_height, 0) * Rot(X=90) * Cylinder(
    center_diameter / 2,
    center_extra_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
center_round_edge = center_raw.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Y)[0]
center_badge = fillet(center_round_edge, center_edge_radius)

publish("outer_badge", outer_badge, "Flat-back outer badge", material="pla")
publish("center_badge", center_badge, "Enlarged center button", material="pla")