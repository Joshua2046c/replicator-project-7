# Bottom half with rounded exterior base, compact external hinge, and split front recess
from build123d import *

overall_length = param("overall_length", 80.0)
outer_width = param("outer_width", 40.0)
bottom_height = param("bottom_height", 16.0)
bottom_outer_fillet = param("bottom_outer_fillet", 2.0)
chamber_diameter = param("chamber_diameter", 35.0)
chamber_depth = param("chamber_depth", 10.0)
wall_thickness = param("wall_thickness", 2.0)
bottom_bowl_sagitta = param("bottom_bowl_sagitta", 0.4)

magnet_diameter = param("magnet_diameter", 6.0)
magnet_depth = param("magnet_depth", 2.0)
magnet_y_from_center = param("magnet_y_from_center", 12.5)

front_recess_diameter = param("front_recess_diameter", 12.0)
front_recess_depth = param("front_recess_depth", 1.8)
front_recess_x = param("front_recess_x", 0.0)
front_recess_z = param("front_recess_z", bottom_height)

hinge_pin_diameter = param("hinge_pin_diameter", 3.0)
hinge_hole_clearance = param("hinge_hole_clearance", 0.3)
hinge_knuckle_diameter = param("hinge_knuckle_diameter", 7.5)
compact_side_knuckle_width = param("compact_side_knuckle_width", 8.0)
compact_center_knuckle_width = param("compact_center_knuckle_width", 14.4)
hinge_axial_gap = param("hinge_axial_gap", 0.3)
hinge_axis_y = param("hinge_axis_y", 24.1)
bottom_hinge_root_y_radius_v5 = param("bottom_hinge_root_y_radius_v5", 2.8)
bottom_hinge_root_z_radius_v5 = param("bottom_hinge_root_z_radius_v5", 2.4)
bottom_hinge_root_y_v5 = param("bottom_hinge_root_y_v5", 20.8)
bottom_hinge_root_z_v5 = param("bottom_hinge_root_z_v5", 13.2)
bottom_hinge_parting_clearance_v3 = param("bottom_hinge_parting_clearance_v3", 0.4)

outer_radius = outer_width / 2
straight_length = overall_length - outer_width
end_center = straight_length / 2
chamber_radius = chamber_diameter / 2
chamber_center = end_center
side_x = compact_center_knuckle_width / 2 + hinge_axial_gap + compact_side_knuckle_width / 2
barrel_radius = hinge_knuckle_diameter / 2
hole_radius = (hinge_pin_diameter + hinge_hole_clearance) / 2
barrel_inner_y = hinge_axis_y - barrel_radius
hinge_shell_clearance = barrel_inner_y - outer_width / 2
minimum_floor_thickness = wall_thickness - bottom_bowl_sagitta
bowl_radius = (chamber_radius ** 2 + bottom_bowl_sagitta ** 2) / (2 * bottom_bowl_sagitta)
bowl_center_z = minimum_floor_thickness + bowl_radius
root_top_z = bottom_hinge_root_z_v5 + bottom_hinge_root_z_radius_v5
root_inner_y = bottom_hinge_root_y_v5 - bottom_hinge_root_y_radius_v5
root_outer_y = bottom_hinge_root_y_v5 + bottom_hinge_root_y_radius_v5
root_to_axis_y = hinge_axis_y - root_outer_y
assert hinge_shell_clearance >= 0.3, "Closed hinge barrel must clear the opposite shell rear wall"
assert root_top_z <= bottom_height - bottom_hinge_parting_clearance_v3, "Lower hinge root must remain below the mating plane"
assert root_inner_y < outer_width / 2, "Lower hinge root must overlap the shell rear wall"
assert root_to_axis_y < barrel_radius, "Lower hinge root must overlap the complete hinge barrel"
assert bottom_bowl_sagitta > 0, "Bottom bowl sagitta must be positive"
assert minimum_floor_thickness >= 1.6, "PLA bottom floor must remain at least 1.6 mm thick"

outer_body = Box(straight_length, outer_width, bottom_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
outer_body = outer_body + Pos(-end_center, 0, 0) * Cylinder(outer_radius, bottom_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
outer_body = outer_body + Pos(end_center, 0, 0) * Cylinder(outer_radius, bottom_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
bottom_perimeter = [edge for edge in outer_body.edges() if abs(edge.center().Z) < 0.01]
body = fillet(bottom_perimeter, radius=bottom_outer_fillet)

magnet_pocket = Pos(0, -magnet_y_from_center, bottom_height - magnet_depth) * Cylinder(
    magnet_diameter / 2, magnet_depth, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
body = body - magnet_pocket

front_recess = Pos(front_recess_x, -outer_width / 2, front_recess_z) * Rot(X=-90) * Cylinder(
    front_recess_diameter / 2, front_recess_depth, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
body = body - front_recess

# Each lower knuckle combines a complete barrel with one low elliptical root.
# The ellipse is buried in the shell and overlaps the barrel below the pin bore,
# creating one continuous rounded load path without entering the mating plane.
for x_pos in (-side_x, side_x):
    with BuildSketch(Plane.YZ) as knuckle_sketch:
        with Locations((hinge_axis_y, bottom_height)):
            Circle(barrel_radius)
        with Locations((bottom_hinge_root_y_v5, bottom_hinge_root_z_v5)):
            Ellipse(bottom_hinge_root_y_radius_v5, bottom_hinge_root_z_radius_v5)
        with Locations((hinge_axis_y, bottom_height)):
            Circle(hole_radius, mode=Mode.SUBTRACT)
    x0 = x_pos - compact_side_knuckle_width / 2
    knuckle = Pos(x0, 0, 0) * extrude(knuckle_sketch.sketch, amount=compact_side_knuckle_width)
    body = (body + knuckle).clean()

# Cut the storage chambers after the hinge fusion. This keeps the chamber rear
# walls continuous and preserves the shallow 0.4 mm bowl profile.
for x_pos in (-chamber_center, chamber_center):
    cavity_cylinder = Pos(x_pos, 0, minimum_floor_thickness - 0.01) * Cylinder(
        chamber_radius,
        chamber_depth + bottom_bowl_sagitta + 0.02,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    cavity_sphere = Pos(x_pos, 0, bowl_center_z) * Sphere(bowl_radius)
    curved_cavity = cavity_cylinder & cavity_sphere
    body = (body - curved_cavity).clean()

bottom_shell = body
publish("bottom_shell", bottom_shell, "Bottom capsule half")