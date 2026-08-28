# Scaled bottom half with matched flat chamber, aligned front recess, and hinge sweep clearance
from build123d import *

target_chamber_diameter = param("target_chamber_diameter", 45.0)
scale_factor = target_chamber_diameter / 35.0
magnet_diameter_v2 = param("magnet_diameter_v2", 8.0)
magnet_depth_v2 = param("magnet_depth_v2", 3.0)
chamber_floor_fillet = param("chamber_floor_fillet", 0.8)
mating_step_height = param("mating_step_height", 3.5)
mating_step_width = param("mating_step_width", 1.4)
mating_step_clearance = param("mating_step_clearance", 0.3)
mating_step_setback = param("mating_step_setback", 0.8)
hinge_step_relief_width = param("hinge_step_relief_width", 63.0)
front_recess_depth = param("front_recess_depth", 2.0)

chamber_diameter = 35.0 * scale_factor
outer_width = 40.0 * scale_factor
overall_length = 80.0 * scale_factor
bottom_height = 16.0 * scale_factor
wall_thickness = 2.0 * scale_factor
magnet_y_from_center = 12.5
front_recess_diameter = 12.0 * scale_factor
front_recess_x = 0.0
front_recess_z = bottom_height
front_recess_entry_overcut = 0.05
hinge_pin_diameter = 3.0 * scale_factor
hinge_hole_clearance = 0.3 * scale_factor
hinge_knuckle_diameter = 7.5 * scale_factor
compact_side_knuckle_width = 8.0 * scale_factor
compact_center_knuckle_width = 14.4 * scale_factor
hinge_axial_gap = 0.3 * scale_factor
hinge_axis_y = 24.1 * scale_factor
bottom_hinge_root_y = param("bottom_hinge_root_y", 27.5)
bottom_hinge_root_y_radius = param("bottom_hinge_root_y_radius", 2.0)
bottom_hinge_root_z_radius = param("bottom_hinge_root_z_radius", 2.4)
bottom_hinge_root_z = bottom_height - 3.0
bottom_hinge_parting_clearance = 0.4 * scale_factor

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
flat_floor_z = wall_thickness
flat_chamber_depth = bottom_height - flat_floor_z
root_top_z = bottom_hinge_root_z + bottom_hinge_root_z_radius
root_inner_y = bottom_hinge_root_y - bottom_hinge_root_y_radius
root_outer_y = bottom_hinge_root_y + bottom_hinge_root_y_radius
root_to_axis_y = hinge_axis_y - root_outer_y

assert abs(target_chamber_diameter - 45.0) < 1e-6, "Scaled chamber target must be 45 mm"
assert abs(flat_chamber_depth - 18.0) < 1e-6, "Lower chamber effective depth must be 18 mm"
assert hinge_shell_clearance >= 0.3 * scale_factor, "Scaled hinge barrel must clear the opposite shell rear wall"
assert root_top_z <= bottom_height - bottom_hinge_parting_clearance + 1e-6, "Lower hinge root must remain below the mating plane"
assert root_inner_y < outer_width / 2, "Lower hinge root must overlap the shell rear wall"
assert root_to_axis_y < barrel_radius, "Lower hinge root must overlap the complete hinge barrel"
assert flat_floor_z >= 2.0, "Flat chamber floor must retain structural PLA thickness"
assert flat_chamber_depth > chamber_floor_fillet, "Flat chamber must have room for the floor transition"
assert chamber_floor_fillet > 0 and chamber_floor_fillet < flat_floor_z, "Chamber floor fillet must fit within the floor thickness"
assert chamber_radius + chamber_floor_fillet < outer_radius - mating_step_setback, "Tongue must remain outside the storage chamber"
assert front_recess_depth > 0, "Front recess depth must be positive"
assert mating_step_height >= 3.0 and mating_step_height <= 4.0, "Mating step height must stay within 3-4 mm"
assert mating_step_width > 0, "Mating step width must be positive"
assert mating_step_clearance > 0, "Mating step clearance must be positive"
assert mating_step_setback > mating_step_clearance, "Mating tongue setback must exceed clearance"
assert hinge_step_relief_width >= outer_width, "Rear hinge relief must cover the complete capsule rear arc"
assert hinge_step_relief_width < overall_length, "Rear hinge relief must leave front locating step material"


def capsule_prism(height, inset=0.0, z=0.0):
    radius = outer_radius - inset
    width = outer_width - 2 * inset
    assert radius > 0 and width > 0, "Capsule inset must leave positive geometry"
    shape = Box(straight_length, width, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    shape = shape + Pos(-end_center, 0, 0) * Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    shape = shape + Pos(end_center, 0, 0) * Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return Pos(0, 0, z) * shape

outer_body = capsule_prism(bottom_height)
bottom_perimeter = [edge for edge in outer_body.edges() if abs(edge.center().Z) < 0.01]
body = fillet(bottom_perimeter, radius=2.0 * scale_factor)

with BuildSketch(Plane.XY) as magnet_sketch:
    with Locations((0, -magnet_y_from_center)):
        Circle(magnet_diameter_v2 / 2)
magnet_pocket = Pos(0, 0, bottom_height - magnet_depth_v2) * extrude(magnet_sketch.sketch, amount=magnet_depth_v2)
body = body - magnet_pocket

# Enter beyond the front skin and stop at the exact 2 mm planar floor datum.
front_recess_start_y = -outer_width / 2 - front_recess_entry_overcut
front_recess = Pos(front_recess_x, front_recess_start_y, front_recess_z) * Rot(X=-90) * Cylinder(
    front_recess_diameter / 2, front_recess_depth + front_recess_entry_overcut, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
body = body - front_recess

for x_pos in (-side_x, side_x):
    with BuildSketch(Plane.YZ) as hinge_outer_sketch:
        with Locations((hinge_axis_y, bottom_height)):
            Circle(barrel_radius)
        with Locations((bottom_hinge_root_y, bottom_hinge_root_z)):
            Ellipse(bottom_hinge_root_y_radius, bottom_hinge_root_z_radius)
        make_hull()
    with BuildSketch(Plane.YZ) as hinge_bore_sketch:
        with Locations((hinge_axis_y, bottom_height)):
            Circle(hole_radius)
    x0 = x_pos - compact_side_knuckle_width / 2
    hinge_outer = Pos(x0, 0, 0) * extrude(hinge_outer_sketch.sketch, amount=compact_side_knuckle_width)
    hinge_bore = Pos(x0, 0, 0) * extrude(hinge_bore_sketch.sketch, amount=compact_side_knuckle_width)
    body = (body + hinge_outer - hinge_bore).clean()

for x_pos in (-chamber_center, chamber_center):
    cavity = Pos(x_pos, 0, flat_floor_z) * Cylinder(chamber_radius, flat_chamber_depth + 0.02, align=(Align.CENTER, Align.CENTER, Align.MIN))
    floor_edges = [edge for edge in cavity.edges() if abs(edge.center().Z - flat_floor_z) < 0.02]
    if floor_edges:
        cavity = fillet(floor_edges, radius=chamber_floor_fillet)
    body = (body - cavity).clean()

# Keep the front locating tongue; the rear 63 mm hinge band is a continuous flat mating plane from Y=0 to the rear edge.
tongue_z = bottom_height - 0.01
tongue_height = mating_step_height + 0.01
tongue_outer = capsule_prism(tongue_height, mating_step_setback, tongue_z)
tongue_inner = capsule_prism(tongue_height, mating_step_setback + mating_step_width, tongue_z)
tongue = tongue_outer - tongue_inner
rear_flat_zone = Pos(0, 0, tongue_z) * Box(hinge_step_relief_width, outer_width / 2, tongue_height, align=(Align.CENTER, Align.MIN, Align.MIN))
tongue = tongue - rear_flat_zone
body = (body + tongue).clean()

bottom_shell = body
publish("bottom_shell", bottom_shell, "Bottom capsule half")