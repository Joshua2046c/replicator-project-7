# Bottom half: fused capsule body with two storage chambers
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
hinge_knuckle_width = param("hinge_knuckle_width", 10.0)
hinge_knuckle_spacing = param("hinge_knuckle_spacing", 25.0)

outer_radius = outer_width / 2
straight_length = overall_length - outer_width
end_center = straight_length / 2
chamber_radius = chamber_diameter / 2
chamber_center = end_center
pin_hole_length = 2 * hinge_knuckle_spacing + hinge_knuckle_width + 2.0
hinge_y = outer_radius - hinge_knuckle_diameter / 2
hinge_z = bottom_height

with BuildPart() as bottom:
    Box(straight_length, outer_width, bottom_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((-end_center, 0, 0), (end_center, 0, 0)):
        Cylinder(outer_radius, bottom_height, align=(Align.CENTER, Align.CENTER, Align.MIN))

    with Locations((-chamber_center, 0, wall_thickness), (chamber_center, 0, wall_thickness)):
        Cylinder(
            chamber_radius,
            chamber_depth,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    for x_pos in (-magnet_x_spacing / 2, magnet_x_spacing / 2):
        with Locations((x_pos, -magnet_y_from_center, bottom_height - magnet_depth)):
            Cylinder(
                magnet_diameter / 2,
                magnet_depth,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )

    # Hinge axis is inset so the knuckles stay within the 40 mm product width.
    with Locations((-hinge_knuckle_spacing, hinge_y, hinge_z), (hinge_knuckle_spacing, hinge_y, hinge_z)):
        Cylinder(
            hinge_knuckle_diameter / 2,
            hinge_knuckle_width,
            rotation=(0, 90, 0),
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
    with Locations((0, hinge_y, hinge_z)):
        Cylinder(
            (hinge_pin_diameter + hinge_hole_clearance) / 2,
            pin_hole_length,
            rotation=(0, 90, 0),
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
            mode=Mode.SUBTRACT,
        )

bottom_shell = bottom.part
publish("bottom_shell", bottom_shell, "Bottom capsule half")
