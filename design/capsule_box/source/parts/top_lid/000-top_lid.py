# Scaled top lid with delayed outer crown, flat chambers, and mating groove
from build123d import *

target_chamber_diameter = param("target_chamber_diameter", 45.0)
scale_factor = target_chamber_diameter / 35.0
magnet_diameter_v2 = param("magnet_diameter_v2", 8.0)
magnet_depth_v2 = param("magnet_depth_v2", 3.0)
chamber_floor_fillet = param("chamber_floor_fillet", 0.8)
top_lid_vertical_land_above_front_slot = param("top_lid_vertical_land_above_front_slot", 3.0)
mating_step_height = param("mating_step_height", 3.5)
mating_step_width = param("mating_step_width", 1.4)
mating_step_clearance = param("mating_step_clearance", 0.3)
mating_step_setback = param("mating_step_setback", 0.8)

chamber_diameter = 35.0 * scale_factor
outer_width = 40.0 * scale_factor
overall_length = 80.0 * scale_factor
lid_height = 16.0 * scale_factor
dome_base_height = 12.0 * scale_factor
inner_clearance = 0.3 * scale_factor
chamber_floor_depth = 3.0 * scale_factor
magnet_y_from_center = 12.5  # Current design default; fixed magnet-interface exception.
front_recess_diameter = 12.0 * scale_factor
front_recess_depth = 1.8 * scale_factor
front_recess_x = 0.0
front_recess_z = 0.0
hinge_pin_diameter = 3.0 * scale_factor
hinge_hole_clearance = 0.3 * scale_factor
hinge_knuckle_diameter = 7.5 * scale_factor
compact_side_knuckle_width = 8.0 * scale_factor
compact_center_knuckle_width = 14.4 * scale_factor
hinge_axial_gap = 0.3 * scale_factor
hinge_axis_y = 24.1 * scale_factor
top_hinge_root_y_radius = 2.8 * scale_factor
top_hinge_root_z_radius = 2.4 * scale_factor
top_hinge_root_y = 20.8 * scale_factor
top_hinge_root_z = 2.85 * scale_factor
top_hinge_parting_clearance = 0.4 * scale_factor

outer_radius = outer_width / 2
straight_length = overall_length - outer_width
end_center = straight_length / 2
chamber_center = end_center
barrel_radius = hinge_knuckle_diameter / 2
hole_radius = (hinge_pin_diameter + hinge_hole_clearance) / 2
barrel_inner_y = hinge_axis_y - barrel_radius
hinge_shell_clearance = barrel_inner_y - outer_width / 2
root_bottom_z = top_hinge_root_z - top_hinge_root_z_radius
root_inner_y = top_hinge_root_y - top_hinge_root_y_radius
root_outer_y = top_hinge_root_y + top_hinge_root_y_radius
root_to_axis = ((hinge_axis_y - top_hinge_root_y) ** 2 + top_hinge_root_z ** 2) ** 0.5
transition_start_z = front_recess_diameter / 2 + top_lid_vertical_land_above_front_slot
outer_top_fillet = lid_height - transition_start_z

assert abs(target_chamber_diameter - 45.0) < 1e-6, "Scaled chamber target must be 45 mm"
assert hinge_shell_clearance >= 0.3 * scale_factor, "Scaled hinge barrel must clear the opposite shell rear wall"
assert root_bottom_z >= top_hinge_parting_clearance, "Upper hinge root must remain above the mating plane"
assert root_inner_y < outer_width / 2, "Upper hinge root must overlap the lid rear wall"
assert hinge_axis_y - root_outer_y < barrel_radius, "Upper hinge root must overlap the complete hinge barrel"
assert root_to_axis > hole_radius + min(top_hinge_root_y_radius, top_hinge_root_z_radius), "Upper hinge root must remain outside the pin bore"
assert transition_start_z > front_recess_diameter / 2, "Outer crown must start above the front half-round slot"
assert outer_top_fillet > 0, "Top crown transition must have positive height"
assert mating_step_height >= 3.0 and mating_step_height <= 4.0, "Mating step height must stay within 3-4 mm"
assert mating_step_width > 0, "Mating step width must be positive"
assert mating_step_clearance > 0, "Mating step clearance must be positive"


def capsule_prism(height, inset=0.0, z=0.0):
    radius = outer_radius - inset
    width = outer_width - 2 * inset
    assert radius > 0 and width > 0, "Capsule inset must leave positive geometry"
    shape = Box(straight_length, width, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    shape = shape + Pos(-end_center, 0, 0) * Cylinder(
        radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    shape = shape + Pos(end_center, 0, 0) * Cylinder(
        radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    return Pos(0, 0, z) * shape


outer_body = capsule_prism(lid_height)
top_edges = [edge for edge in outer_body.edges() if abs(edge.center().Z - lid_height) < 0.01]
if top_edges:
    outer_body = fillet(top_edges, radius=outer_top_fillet)

# Flat circular chambers with a small floor-to-wall transition radius.
for x_pos in (-chamber_center, chamber_center):
    cavity = Pos(x_pos, 0, -0.01) * Cylinder(
        chamber_diameter / 2,
        chamber_floor_depth + 0.01,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    floor_edges = [edge for edge in cavity.edges() if edge.center().Z > chamber_floor_depth - 0.02]
    if floor_edges:
        cavity = fillet(floor_edges, radius=chamber_floor_fillet)
    outer_body = outer_body - cavity

# Explicit circular magnet pocket; diameter, depth, and Y position stay fixed.
with BuildSketch(Plane.XY) as magnet_sketch:
    with Locations((0, -magnet_y_from_center)):
        Circle(magnet_diameter_v2 / 2)
magnet_pocket = Pos(0, 0, -0.01) * extrude(
    magnet_sketch.sketch,
    amount=magnet_depth_v2 + 0.01,
)
body = outer_body - magnet_pocket

front_recess = Pos(front_recess_x, -outer_width / 2, front_recess_z) * Rot(X=-90) * Cylinder(
    front_recess_diameter / 2,
    front_recess_depth,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
body = body - front_recess

# Continuous upper recess for the lower perimeter tongue. The two inset boundaries
# leave a 0.3 mm radial clearance around the nominal lower tongue.
groove_outer_inset = mating_step_setback - mating_step_clearance
groove_inner_inset = mating_step_setback + mating_step_width + mating_step_clearance
groove_outer = capsule_prism(mating_step_height + 0.02, groove_outer_inset, -0.01)
groove_inner = capsule_prism(mating_step_height + 0.02, groove_inner_inset, -0.01)
groove_ring = groove_outer - groove_inner
body = body - groove_ring

# One continuous convex outer section blends the complete barrel into the lid wall,
# then cuts the circular bore separately to preserve a complete 360-degree sleeve.
with BuildSketch(Plane.YZ) as hinge_outer_sketch:
    with Locations((hinge_axis_y, 0)):
        Circle(barrel_radius)
    with Locations((top_hinge_root_y, top_hinge_root_z)):
        Ellipse(top_hinge_root_y_radius, top_hinge_root_z_radius)
    make_hull()
with BuildSketch(Plane.YZ) as hinge_bore_sketch:
    with Locations((hinge_axis_y, 0)):
        Circle(hole_radius)
center_knuckle = Pos(-compact_center_knuckle_width / 2, 0, 0) * (
    extrude(hinge_outer_sketch.sketch, amount=compact_center_knuckle_width)
    - extrude(hinge_bore_sketch.sketch, amount=compact_center_knuckle_width)
)
top_lid = (body + center_knuckle).clean()
publish("top_lid", top_lid, "Top capsule lid")