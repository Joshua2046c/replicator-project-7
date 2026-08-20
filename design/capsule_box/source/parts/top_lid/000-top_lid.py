# Top lid: deep capsule cover with one central hinge knuckle
from build123d import *

overall_length = param("overall_length", 80.0)
outer_width = param("outer_width", 40.0)
lid_height = param("lid_height", 12.0)
inner_clearance = param("inner_clearance", 0.3)
chamber_diameter = param("chamber_diameter", 35.0)
relief_depth = param("relief_depth", 10.0)

magnet_diameter = param("magnet_diameter", 6.0)
magnet_depth = param("magnet_depth", 2.2)
magnet_x_spacing = param("magnet_x_spacing", 10.0)
magnet_y_from_center = param("magnet_y_from_center", 16.0)

hinge_pin_diameter = param("hinge_pin_diameter", 3.0)
hinge_hole_clearance = param("hinge_hole_clearance", 0.3)
hinge_knuckle_diameter = param("hinge_knuckle_diameter", 6.0)
hinge_center_width = param("hinge_center_width", 39.4)

outer_radius = outer_width / 2
straight_length = overall_length - outer_width
end_center = straight_length / 2
chamber_center = end_center
hinge_y = outer_radius - hinge_knuckle_diameter / 2
pin_hole_length = 62.0

body = Box(
    straight_length,
    outer_width,
    lid_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
body = body + Pos(-end_center, 0, 0) * Cylinder(
    outer_radius, lid_height, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
body = body + Pos(end_center, 0, 0) * Cylinder(
    outer_radius, lid_height, align=(Align.CENTER, Align.CENTER, Align.MIN)
)

relief_radius = chamber_diameter / 2 + inner_clearance
left_relief = Pos(-chamber_center, 0, -0.01) * Cylinder(
    relief_radius, relief_depth + 0.01, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
right_relief = Pos(chamber_center, 0, -0.01) * Cylinder(
    relief_radius, relief_depth + 0.01, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
lid_shell = body - left_relief - right_relief

for x_pos in (-magnet_x_spacing / 2, magnet_x_spacing / 2):
    pocket = Pos(x_pos, -magnet_y_from_center, -0.01) * Cylinder(
        magnet_diameter / 2,
        magnet_depth + 0.01,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    lid_shell = lid_shell - pocket

central_knuckle = Pos(0, hinge_y, 0) * Rot(Y=90) * Cylinder(
    hinge_knuckle_diameter / 2,
    hinge_center_width,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)
lid_with_hinge = lid_shell + central_knuckle

pin_hole = Pos(0, hinge_y, 0) * Rot(Y=90) * Cylinder(
    (hinge_pin_diameter + hinge_hole_clearance) / 2,
    pin_hole_length,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)
top_lid = lid_with_hinge - pin_hole
publish("top_lid", top_lid, "Top capsule lid")
