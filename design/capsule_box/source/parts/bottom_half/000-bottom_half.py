# cell: bottom_half
# Bottom capsule half: flat mating rim, flat chamber floors, and a vertical front recess wall.
from build123d import *

target_chamber_diameter = param("target_chamber_diameter", 45.0)
scale_factor = target_chamber_diameter / 35.0
magnet_diameter_v2 = param("magnet_diameter_v2", 8.0)
magnet_depth_v2 = param("magnet_depth_v2", 3.0)
chamber_floor_fillet = param("chamber_floor_fillet", 0.8)
front_recess_depth = param("front_recess_depth", 2.0)
original_hinge_knuckle_diameter = param("original_hinge_knuckle_diameter", 6.0)
hinge_side_ear_width_v4 = param("hinge_side_ear_width_v4", 10.0 / 3.0)
hinge_side_center_spacing_v4 = param("hinge_side_center_spacing_v4", 25.0 / 3.0)
hinge_root_embed_v4 = param("hinge_root_embed_v4", 0.2)
front_recess_center_offset_v3 = param("front_recess_center_offset_v3", 0.0)

chamber_diameter = 35.0 * scale_factor
outer_width = 40.0 * scale_factor
overall_length = 80.0 * scale_factor
bottom_height = 16.0 * scale_factor
wall_thickness = 2.0 * scale_factor
magnet_y_from_center = 12.5
hinge_pin_diameter = 3.0 * scale_factor
hinge_hole_clearance = 0.3 * scale_factor
front_recess_diameter = 12.0 * scale_factor
front_recess_x = 0.0
front_recess_entry_overcut = 0.05

outer_radius = outer_width / 2
straight_length = overall_length - outer_width
end_center = straight_length / 2
chamber_radius = chamber_diameter / 2
chamber_center = end_center
barrel_radius = original_hinge_knuckle_diameter * scale_factor / 2
side_knuckle_width = hinge_side_ear_width_v4 * scale_factor
side_x = hinge_side_center_spacing_v4 * scale_factor
# The circular knuckle is tangent to the rear wall; there is no rectangular ear-root block.
hinge_axis_y = outer_radius + barrel_radius - hinge_root_embed_v4
hole_radius = (hinge_pin_diameter + hinge_hole_clearance) / 2
flat_floor_z = wall_thickness
flat_chamber_depth = bottom_height - flat_floor_z
front_recess_center_z = bottom_height + front_recess_center_offset_v3

assert abs(target_chamber_diameter - 45.0) < 1e-6
assert abs(flat_chamber_depth - 18.0) < 1e-6
assert abs(front_recess_center_z - bottom_height) < 1e-6
assert hinge_axis_y - barrel_radius < outer_radius + 1e-6
assert side_x - side_knuckle_width / 2 > 0
assert flat_floor_z >= 2.0
assert flat_chamber_depth > chamber_floor_fillet
assert chamber_floor_fillet > 0 and chamber_floor_fillet < flat_floor_z
assert front_recess_depth > 0

def capsule_prism(height, inset=0.0, z=0.0):
    radius = outer_radius - inset
    width = outer_width - 2 * inset
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

for x_pos in (-side_x, side_x):
    hinge_outer = Pos(x_pos, hinge_axis_y, bottom_height) * Rot(Y=90) * Cylinder(
        barrel_radius, side_knuckle_width,
        align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    hinge_bore = Pos(x_pos, hinge_axis_y, bottom_height) * Rot(Y=90) * Cylinder(
        hole_radius, side_knuckle_width,
        align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    body = (body + hinge_outer - hinge_bore).clean()

for x_pos in (-chamber_center, chamber_center):
    cavity = Pos(x_pos, 0, flat_floor_z) * Cylinder(
        chamber_radius, flat_chamber_depth + 0.02,
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    floor_edges = [edge for edge in cavity.edges() if abs(edge.center().Z - flat_floor_z) < 0.02]
    if floor_edges:
        cavity = fillet(floor_edges, radius=chamber_floor_fillet)
    body = (body - cavity).clean()

# No mating tongue: the rim is a continuous flat plane.
# One axis-normal cylinder gives a centered recess with vertical circular walls and a flat floor.
front_recess_start_y = -outer_width / 2 - front_recess_entry_overcut
front_recess = Pos(front_recess_x, front_recess_start_y, front_recess_center_z) * Rot(X=-90) * Cylinder(
    front_recess_diameter / 2,
    front_recess_depth + front_recess_entry_overcut,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
body = (body - front_recess).clean()

bottom_shell = body
publish("bottom_shell", bottom_shell, "Bottom capsule half")