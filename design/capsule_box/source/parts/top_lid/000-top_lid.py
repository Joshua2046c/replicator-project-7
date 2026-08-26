# Top lid with the whole outer cover rolled into one large-radius crown and split front recess
from build123d import *

overall_length = param("overall_length", 80.0)
outer_width = param("outer_width", 40.0)
lid_height = param("lid_height", 16.0)
dome_base_height = param("dome_base_height", 12.0)
dome_sagitta = param("dome_sagitta", 4.0)
dome_transition_fillet = param("dome_transition_fillet", 2.0)
outer_top_fillet = param("outer_top_fillet", 15.0)
inner_clearance = param("inner_clearance", 0.3)
chamber_diameter = param("chamber_diameter", 35.0)
relief_depth = param("relief_depth", 10.0)

magnet_diameter = param("magnet_diameter", 6.0)
magnet_depth = param("magnet_depth", 2.2)
magnet_y_from_center = param("magnet_y_from_center", 12.5)

front_recess_diameter = param("front_recess_diameter", 12.0)
front_recess_depth = param("front_recess_depth", 1.8)
front_recess_x = param("front_recess_x", 0.0)
front_recess_z = param("front_recess_z", 0.0)

hinge_pin_diameter = param("hinge_pin_diameter", 3.0)
hinge_hole_clearance = param("hinge_hole_clearance", 0.3)
hinge_knuckle_diameter = param("hinge_knuckle_diameter", 6.0)
compact_side_knuckle_width = param("compact_side_knuckle_width", 8.0)
compact_center_knuckle_width = param("compact_center_knuckle_width", 14.4)
hinge_axial_gap = param("hinge_axial_gap", 0.3)
hinge_axis_y = param("hinge_axis_y", 23.0)
hinge_neck_depth = param("hinge_neck_depth", 5.0)
hinge_neck_height = param("hinge_neck_height", 3.0)
hinge_root_fillet = param("hinge_root_fillet", 3.5)
top_hinge_root_rise = param("top_hinge_root_rise", 4.0)
top_hinge_root_pull = param("top_hinge_root_pull", 1.6)

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

top_edges = [edge for edge in outer_body.edges() if abs(edge.center().Z - lid_height) < 0.01]
if top_edges:
    outer_body = fillet(top_edges, radius=outer_top_fillet)

relief_radius = chamber_diameter / 2 + inner_clearance
for x_pos in (-chamber_center, chamber_center):
    relief = Pos(x_pos, 0, -0.01) * Cylinder(
        relief_radius,
        relief_depth + 0.01,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    outer_body = outer_body - relief

magnet_pocket = Pos(0, -magnet_y_from_center, -0.01) * Cylinder(
    magnet_diameter / 2,
    magnet_depth + 0.01,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
body = outer_body - magnet_pocket

front_recess = Pos(
    front_recess_x,
    -outer_width / 2,
    front_recess_z,
) * Rot(X=-90) * Cylinder(
    front_recess_diameter / 2,
    front_recess_depth,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
body = body - front_recess

# The upper knuckle mirrors the lower tangent topology and anchors directly on
# the actual rear wall. The lower curve is tangent to the mating plane, the
# upper curve is tangent to the rear wall, and both meet the barrel smoothly.
barrel_radius = hinge_knuckle_diameter / 2
shell_wall_y = outer_width / 2
root_upper_z = top_hinge_root_rise
with BuildSketch(Plane.YZ) as root_sketch:
    with BuildLine():
        Line((shell_wall_y, root_upper_z), (shell_wall_y, 0))
        Bezier(
            (shell_wall_y, 0),
            (shell_wall_y + top_hinge_root_pull, 0),
            (hinge_axis_y - top_hinge_root_pull, -barrel_radius),
            (hinge_axis_y, -barrel_radius),
        )
        ThreePointArc(
            (hinge_axis_y, -barrel_radius),
            (hinge_axis_y + barrel_radius, 0),
            (hinge_axis_y, barrel_radius),
        )
        Bezier(
            (hinge_axis_y, barrel_radius),
            (hinge_axis_y - top_hinge_root_pull, barrel_radius),
            (shell_wall_y, root_upper_z - top_hinge_root_pull),
            (shell_wall_y, root_upper_z),
        )
    make_face()
root_transition = Pos(-compact_center_knuckle_width / 2, 0, 0) * extrude(
    root_sketch.sketch, amount=compact_center_knuckle_width
)
lid_with_hinge = body + root_transition

pin_hole = Pos(0, hinge_axis_y, 0) * Rot(Y=90) * Cylinder(
    (hinge_pin_diameter + hinge_hole_clearance) / 2,
    pin_hole_length,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)
top_lid = lid_with_hinge - pin_hole
publish("top_lid", top_lid, "Top capsule lid")