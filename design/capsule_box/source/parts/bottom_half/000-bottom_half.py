# Bottom half with compact external three-knuckle hinge
from build123d import *

overall_length = param("overall_length", 80.0)
outer_width = param("outer_width", 40.0)
bottom_height = param("bottom_height", 13.0)
chamber_diameter = param("chamber_diameter", 35.0)
chamber_depth = param("chamber_depth", 10.0)
wall_thickness = param("wall_thickness", 2.0)

magnet_diameter = param("magnet_diameter", 6.0)
magnet_depth = param("magnet_depth", 2.2)
magnet_x_spacing = param("magnet_x_spacing", 10.0)
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
chamber_radius = chamber_diameter / 2
chamber_center = end_center
side_x = compact_center_knuckle_width / 2 + hinge_axial_gap + compact_side_knuckle_width / 2
hinge_span = 2 * compact_side_knuckle_width + compact_center_knuckle_width + 2 * hinge_axial_gap
pin_hole_length = hinge_span + 1.0

body = Box(
    straight_length,
    outer_width,
    bottom_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
body = body + Pos(-end_center, 0, 0) * Cylinder(
    outer_radius, bottom_height, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
body = body + Pos(end_center, 0, 0) * Cylinder(
    outer_radius, bottom_height, align=(Align.CENTER, Align.CENTER, Align.MIN)
)

for x_pos in (-chamber_center, chamber_center):
    cavity = Pos(x_pos, 0, wall_thickness) * Cylinder(
        chamber_radius,
        chamber_depth,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    body = body - cavity

for x_pos in (-magnet_x_spacing / 2, magnet_x_spacing / 2):
    pocket = Pos(x_pos, -magnet_y_from_center, bottom_height - magnet_depth) * Cylinder(
        magnet_diameter / 2,
        magnet_depth,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    body = body - pocket

# Two short side knuckles are confined to the solid center bridge.
for x_pos in (-side_x, side_x):
    neck = Pos(x_pos, outer_width / 2 + hinge_neck_depth / 2 - 1.0, bottom_height - hinge_neck_height / 2) * Box(
        compact_side_knuckle_width,
        hinge_neck_depth,
        hinge_neck_height,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    knuckle = Pos(x_pos, hinge_axis_y, bottom_height) * Rot(Y=90) * Cylinder(
        hinge_knuckle_diameter / 2,
        compact_side_knuckle_width,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    body = body + neck + knuckle

pin_hole = Pos(0, hinge_axis_y, bottom_height) * Rot(Y=90) * Cylinder(
    (hinge_pin_diameter + hinge_hole_clearance) / 2,
    pin_hole_length,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)
bottom_shell = body - pin_hole
publish("bottom_shell", bottom_shell, "Bottom capsule half")
