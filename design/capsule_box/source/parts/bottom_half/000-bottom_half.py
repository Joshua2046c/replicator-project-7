# Bottom half with rounded exterior base, compact external hinge, and split front recess
from build123d import *

overall_length = param("overall_length", 80.0)
outer_width = param("outer_width", 40.0)
bottom_height = param("bottom_height", 16.0)
bottom_outer_fillet = param("bottom_outer_fillet", 2.0)
chamber_diameter = param("chamber_diameter", 35.0)
chamber_depth = param("chamber_depth", 10.0)
wall_thickness = param("wall_thickness", 2.0)

magnet_diameter = param("magnet_diameter", 6.0)
magnet_depth = param("magnet_depth", 2.2)
magnet_y_from_center = param("magnet_y_from_center", 12.5)

front_recess_diameter = param("front_recess_diameter", 12.0)
front_recess_depth = param("front_recess_depth", 1.8)
front_recess_x = param("front_recess_x", 0.0)
front_recess_z = param("front_recess_z", bottom_height)

hinge_pin_diameter = param("hinge_pin_diameter", 3.0)
hinge_hole_clearance = param("hinge_hole_clearance", 0.3)
hinge_knuckle_diameter = param("hinge_knuckle_diameter", 6.0)
compact_side_knuckle_width = param("compact_side_knuckle_width", 8.0)
compact_center_knuckle_width = param("compact_center_knuckle_width", 14.4)
hinge_axial_gap = param("hinge_axial_gap", 0.3)
hinge_axis_y = param("hinge_axis_y", 23.0)
hinge_neck_depth = param("hinge_neck_depth", 5.0)
hinge_neck_height = param("hinge_neck_height", 3.0)
hinge_root_fillet = param("hinge_root_fillet", 1.35)
bottom_hinge_root_drop = param("bottom_hinge_root_drop", 4.0)
bottom_hinge_root_pull = param("bottom_hinge_root_pull", 1.6)

outer_radius = outer_width / 2
straight_length = overall_length - outer_width
end_center = straight_length / 2
chamber_radius = chamber_diameter / 2
chamber_center = end_center
side_x = compact_center_knuckle_width / 2 + hinge_axial_gap + compact_side_knuckle_width / 2
hinge_span = 2 * compact_side_knuckle_width + compact_center_knuckle_width + 2 * hinge_axial_gap
pin_hole_length = hinge_span + 1.0

outer_body = Box(straight_length, outer_width, bottom_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
outer_body = outer_body + Pos(-end_center, 0, 0) * Cylinder(outer_radius, bottom_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
outer_body = outer_body + Pos(end_center, 0, 0) * Cylinder(outer_radius, bottom_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
bottom_perimeter = [edge for edge in outer_body.edges() if abs(edge.center().Z) < 0.01]
body = fillet(bottom_perimeter, radius=bottom_outer_fillet)

for x_pos in (-chamber_center, chamber_center):
    cavity = Pos(x_pos, 0, wall_thickness) * Cylinder(chamber_radius, chamber_depth, align=(Align.CENTER, Align.CENTER, Align.MIN))
    body = body - cavity

magnet_pocket = Pos(0, -magnet_y_from_center, bottom_height - magnet_depth) * Cylinder(
    magnet_diameter / 2, magnet_depth, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
body = body - magnet_pocket

front_recess = Pos(front_recess_x, -outer_width / 2, front_recess_z) * Rot(X=-90) * Cylinder(
    front_recess_diameter / 2, front_recess_depth, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
body = body - front_recess

# Each lower knuckle is one tangent teardrop section anchored on the actual
# shell boundary. The top curve is tangent to the mating plane, the lower curve
# is tangent to the rear wall, and both meet the barrel without a shoulder.
barrel_radius = hinge_knuckle_diameter / 2
shell_wall_y = outer_width / 2
root_lower_z = bottom_height - bottom_hinge_root_drop
for x_pos in (-side_x, side_x):
    with BuildSketch(Plane.YZ) as root_sketch:
        with BuildLine():
            Line((shell_wall_y, root_lower_z), (shell_wall_y, bottom_height))
            Bezier(
                (shell_wall_y, bottom_height),
                (shell_wall_y + bottom_hinge_root_pull, bottom_height),
                (hinge_axis_y - bottom_hinge_root_pull, bottom_height + barrel_radius),
                (hinge_axis_y, bottom_height + barrel_radius),
            )
            ThreePointArc(
                (hinge_axis_y, bottom_height + barrel_radius),
                (hinge_axis_y + barrel_radius, bottom_height),
                (hinge_axis_y, bottom_height - barrel_radius),
            )
            Bezier(
                (hinge_axis_y, bottom_height - barrel_radius),
                (hinge_axis_y - bottom_hinge_root_pull, bottom_height - barrel_radius),
                (shell_wall_y, root_lower_z + bottom_hinge_root_pull),
                (shell_wall_y, root_lower_z),
            )
        make_face()
    x0 = x_pos - compact_side_knuckle_width / 2
    root_profile = Pos(x0, 0, 0) * extrude(root_sketch.sketch, amount=compact_side_knuckle_width)
    body = body + root_profile

pin_hole = Pos(0, hinge_axis_y, bottom_height) * Rot(Y=90) * Cylinder(
    (hinge_pin_diameter + hinge_hole_clearance) / 2, pin_hole_length, align=(Align.CENTER, Align.CENTER, Align.CENTER)
)
bottom_shell = body - pin_hole
publish("bottom_shell", bottom_shell, "Bottom capsule half")