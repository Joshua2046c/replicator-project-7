# cell: top_lid
# Top capsule lid with a continuous flat mating rim and vertical front recess wall.
from build123d import *

target_chamber_diameter = param("target_chamber_diameter", 45.0)
scale_factor = target_chamber_diameter / 35.0
magnet_diameter_v2 = param("magnet_diameter_v2", 8.0)
magnet_depth_v2 = param("magnet_depth_v2", 3.0)
chamber_floor_fillet = param("chamber_floor_fillet", 0.8)
top_lid_vertical_land_above_front_slot = param("top_lid_vertical_land_above_front_slot", 3.0)
chamber_depth = param("chamber_depth", 18.0)
front_recess_depth = param("front_recess_depth", 2.0)
original_hinge_knuckle_diameter = param("original_hinge_knuckle_diameter", 6.0)
hinge_center_ear_width_v4 = param("hinge_center_ear_width_v4", 39.4 / 3.0)
hinge_root_embed_v4 = param("hinge_root_embed_v4", 0.2)

chamber_diameter = 35.0 * scale_factor
outer_width = 40.0 * scale_factor
overall_length = 80.0 * scale_factor
lid_height = 16.0 * scale_factor
wall_thickness = 2.0 * scale_factor
magnet_y_from_center = 12.5
front_recess_diameter = 12.0 * scale_factor
front_recess_x = 0.0
front_recess_center_z = 0.0
front_recess_entry_overcut = 0.05
hinge_pin_diameter = 3.0 * scale_factor
hinge_hole_clearance = 0.3 * scale_factor

outer_radius = outer_width / 2
straight_length = overall_length - outer_width
end_center = straight_length / 2
chamber_center = end_center
barrel_radius = original_hinge_knuckle_diameter * scale_factor / 2
center_knuckle_width = hinge_center_ear_width_v4 * scale_factor
hole_radius = (hinge_pin_diameter + hinge_hole_clearance) / 2
# Same tangent axis as the lower knuckles; no rectangular upper ear-root block.
hinge_axis_y = outer_radius + barrel_radius - hinge_root_embed_v4
flat_floor_z = wall_thickness
flat_chamber_depth = chamber_depth
transition_start_z = front_recess_diameter / 2 + top_lid_vertical_land_above_front_slot
outer_top_fillet = lid_height - transition_start_z

assert abs(target_chamber_diameter - 45.0) < 1e-6
assert abs(chamber_depth - 18.0) < 1e-6
assert abs(chamber_depth + wall_thickness - lid_height) < 1e-6
assert hinge_axis_y - barrel_radius < outer_radius + 1e-6
assert center_knuckle_width > 0
assert front_recess_depth > 0

def capsule_prism(height, inset=0.0, z=0.0):
    radius = outer_radius - inset
    width = outer_width - 2 * inset
    shape = Box(straight_length, width, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    shape = shape + Pos(-end_center, 0, 0) * Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    shape = shape + Pos(end_center, 0, 0) * Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return Pos(0, 0, z) * shape

outer_body = capsule_prism(lid_height)
top_edges = [edge for edge in outer_body.edges() if abs(edge.center().Z - lid_height) < 0.01]
if top_edges:
    outer_body = fillet(top_edges, radius=outer_top_fillet)

for x_pos in (-chamber_center, chamber_center):
    cavity = Pos(x_pos, 0, -0.01) * Cylinder(
        chamber_diameter / 2, chamber_depth + 0.01,
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    floor_edges = [edge for edge in cavity.edges() if edge.center().Z > chamber_depth - 0.02]
    if floor_edges:
        cavity = fillet(floor_edges, radius=chamber_floor_fillet)
    outer_body = outer_body - cavity

with BuildSketch(Plane.XY) as magnet_sketch:
    with Locations((0, -magnet_y_from_center)):
        Circle(magnet_diameter_v2 / 2)
magnet_pocket = Pos(0, 0, -0.01) * extrude(magnet_sketch.sketch, amount=magnet_depth_v2 + 0.01)
body = outer_body - magnet_pocket

# No mating groove and no separate backfill disk: the underside and recess floor are continuous.
front_recess_start_y = -outer_width / 2 - front_recess_entry_overcut
front_recess = Pos(front_recess_x, front_recess_start_y, front_recess_center_z) * Rot(X=-90) * Cylinder(
    front_recess_diameter / 2,
    front_recess_depth + front_recess_entry_overcut,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
body = (body - front_recess).clean()

center_knuckle = Pos(0, hinge_axis_y, 0) * Rot(Y=90) * Cylinder(
    barrel_radius, center_knuckle_width,
    align=(Align.CENTER, Align.CENTER, Align.CENTER)
)
center_bore = Pos(0, hinge_axis_y, 0) * Rot(Y=90) * Cylinder(
    hole_radius, center_knuckle_width,
    align=(Align.CENTER, Align.CENTER, Align.CENTER)
)
body = (body + center_knuckle - center_bore).clean()
top_lid = body
publish("top_lid", top_lid, "Top capsule lid")