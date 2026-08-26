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
relief_depth = param("relief_depth", 3.0)
inner_bowl_sagitta = param("inner_bowl_sagitta", 2.0)

magnet_diameter = param("magnet_diameter", 6.0)
magnet_depth = param("magnet_depth", 2.0)
magnet_y_from_center = param("magnet_y_from_center", 12.5)

front_recess_diameter = param("front_recess_diameter", 12.0)
front_recess_depth = param("front_recess_depth", 1.8)
front_recess_x = param("front_recess_x", 0.0)
front_recess_z = param("front_recess_z", 0.0)

hinge_pin_diameter = param("hinge_pin_diameter", 3.0)
hinge_hole_clearance = param("hinge_hole_clearance", 0.3)
hinge_knuckle_diameter = param("hinge_knuckle_diameter", 7.5)
compact_side_knuckle_width = param("compact_side_knuckle_width", 8.0)
compact_center_knuckle_width = param("compact_center_knuckle_width", 14.4)
hinge_axial_gap = param("hinge_axial_gap", 0.3)
hinge_axis_y = param("hinge_axis_y", 24.1)
top_hinge_root_y_radius_v2 = param("top_hinge_root_y_radius_v2", 2.8)
top_hinge_root_z_radius_v2 = param("top_hinge_root_z_radius_v2", 2.4)
top_hinge_root_y_v2 = param("top_hinge_root_y_v2", 20.8)
top_hinge_root_z_v2 = param("top_hinge_root_z_v2", 2.85)
top_hinge_parting_clearance_v2 = param("top_hinge_parting_clearance_v2", 0.4)

outer_radius = outer_width / 2
straight_length = overall_length - outer_width
end_center = straight_length / 2
chamber_center = end_center
barrel_radius = hinge_knuckle_diameter / 2
hole_radius = (hinge_pin_diameter + hinge_hole_clearance) / 2
barrel_inner_y = hinge_axis_y - barrel_radius
hinge_shell_clearance = barrel_inner_y - outer_width / 2
relief_radius = chamber_diameter / 2 + inner_clearance
bowl_radius = (relief_radius ** 2 + inner_bowl_sagitta ** 2) / (2 * inner_bowl_sagitta)
bowl_center_z = relief_depth + inner_bowl_sagitta - bowl_radius
bowl_max_depth = relief_depth + inner_bowl_sagitta
root_bottom_z = top_hinge_root_z_v2 - top_hinge_root_z_radius_v2
root_inner_y = top_hinge_root_y_v2 - top_hinge_root_y_radius_v2
root_outer_y = top_hinge_root_y_v2 + top_hinge_root_y_radius_v2
root_to_axis = ((hinge_axis_y - top_hinge_root_y_v2) ** 2 + top_hinge_root_z_v2 ** 2) ** 0.5
assert hinge_shell_clearance >= 0.3, "Closed hinge barrel must clear the opposite shell rear wall"
assert root_bottom_z >= top_hinge_parting_clearance_v2, "Upper hinge root must remain above the mating plane"
assert root_inner_y < outer_width / 2, "Upper hinge root must overlap the lid rear wall"
assert hinge_axis_y - root_outer_y < barrel_radius, "Upper hinge root must overlap the complete hinge barrel"
assert root_to_axis > hole_radius + min(top_hinge_root_y_radius_v2, top_hinge_root_z_radius_v2), "Upper hinge root must remain outside the pin bore"
assert inner_bowl_sagitta > 0, "Inner bowl sagitta must be positive"
assert bowl_max_depth <= dome_base_height, "Inner bowl must not extend above the outer dome transition height"

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

# Each chamber keeps the original circular opening and edge depth, while a large
# spherical cutter raises the center by the sagitta to create a shallow bowl.
for x_pos in (-chamber_center, chamber_center):
    relief_cylinder = Pos(x_pos, 0, -0.01) * Cylinder(
        relief_radius,
        bowl_max_depth + 0.02,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    relief_sphere = Pos(x_pos, 0, bowl_center_z) * Sphere(bowl_radius)
    curved_relief = relief_cylinder & relief_sphere
    outer_body = outer_body - curved_relief

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

# The center knuckle combines a complete barrel with one upper elliptical root.
# The root stays above the mating plane and overlaps the rear wall and barrel,
# removing the former tapered web and abrupt shoulder without opening the bore.
with BuildSketch(Plane.YZ) as outer_sketch:
    with Locations((hinge_axis_y, 0)):
        Circle(barrel_radius)
    with Locations((top_hinge_root_y_v2, top_hinge_root_z_v2)):
        Ellipse(top_hinge_root_y_radius_v2, top_hinge_root_z_radius_v2)
    with Locations((hinge_axis_y, 0)):
        Circle(hole_radius, mode=Mode.SUBTRACT)
center_knuckle = Pos(-compact_center_knuckle_width / 2, 0, 0) * extrude(
    outer_sketch.sketch, amount=compact_center_knuckle_width
)
top_lid = (body + center_knuckle).clean()
publish("top_lid", top_lid, "Top capsule lid")