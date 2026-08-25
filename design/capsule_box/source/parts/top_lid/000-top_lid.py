# Top lid with rounded crown and compact external center hinge knuckle
from build123d import *

overall_length = param("overall_length", 80.0)
outer_width = param("outer_width", 40.0)
lid_height = param("lid_height", 14.0)
top_outer_fillet = param("top_outer_fillet", 3.0)
inner_clearance = param("inner_clearance", 0.3)
chamber_diameter = param("chamber_diameter", 35.0)
relief_depth = param("relief_depth", 10.0)

magnet_diameter = param("magnet_diameter", 6.0)
magnet_depth = param("magnet_depth", 2.2)
magnet_y_from_center = param("magnet_y_from_center", 16.0)

hinge_pin_diameter = param("hinge_pin_diameter", 3.0)
hinge_hole_clearance = param("hinge_hole_clearance", 0.3)
hinge_knuckle_diameter = param("hinge_knuckle_diameter", 6.0)
compact_side_knuckle_width = param("compact_side_knuckle_width", 8.0)
compact_center_knuckle_width = param("compact_center_knuckle_width", 14.4)
hinge_axial_gap = param("hinge_axial_gap", 0.3)
hinge_axis_y = param("hinge_axis_y", 23.0)
hinge_neck_depth = param("hinge_neck_depth", 5.0)
hinge_neck_height = param("hinge_neck_height", 3.0)

outer_radius = outer_width / 2
straight_length = overall_length - outer_width
end_center = straight_length / 2
chamber_center = end_center
hinge_span = 2 * compact_side_knuckle_width + compact_center_knuckle_width + 2 * hinge_axial_gap
pin_hole_length = hinge_span + 1.0

outer_body = Box(
    straight_length,
    outer_width,
    lid_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
outer_body = outer_body + Pos(-end_center, 0, 0) * Cylinder(
    outer_radius, lid_height, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
outer_body = outer_body + Pos(end_center, 0, 0) * Cylinder(
    outer_radius, lid_height, align=(Align.CENTER, Align.CENTER, Align.MIN)
)

# Round only the upper exterior perimeter to create a shallow crown.
top_perimeter = [edge for edge in outer_body.edges() if abs(edge.center().Z - lid_height) < 0.01]
body = fillet(top_perimeter, radius=top_outer_fillet)

relief_radius = chamber_diameter / 2 + inner_clearance
for x_pos in (-chamber_center, chamber_center):
    relief = Pos(x_pos, 0, -0.01) * Cylinder(
        relief_radius,
        relief_depth + 0.01,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    body = body - relief

magnet_pocket = Pos(0, -magnet_y_from_center, -0.01) * Cylinder(
    magnet_diameter / 2,
    magnet_depth + 0.01,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
body = body - magnet_pocket

neck = Pos(0, outer_width / 2 + hinge_neck_depth / 2 - 1.0, hinge_neck_height / 2) * Box(
    compact_center_knuckle_width,
    hinge_neck_depth,
    hinge_neck_height,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)
knuckle = Pos(0, hinge_axis_y, 0) * Rot(Y=90) * Cylinder(
    hinge_knuckle_diameter / 2,
    compact_center_knuckle_width,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)
lid_with_hinge = body + neck + knuckle

pin_hole = Pos(0, hinge_axis_y, 0) * Rot(Y=90) * Cylinder(
    (hinge_pin_diameter + hinge_hole_clearance) / 2,
    pin_hole_length,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)
top_lid = lid_with_hinge - pin_hole
publish("top_lid", top_lid, "Top capsule lid")
