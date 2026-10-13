# cell: bottom_cavity_liner
# Removable liner for one bottom-half chamber.
from build123d import *

bottom_liner_outer_diameter = param("bottom_liner_outer_diameter", 44.5)
bottom_liner_height = param("bottom_liner_height", 16.0)
bottom_liner_wall_thickness = param("bottom_liner_wall_thickness", 1.3)
bottom_liner_bottom_thickness = param("bottom_liner_bottom_thickness", 1.7)
bottom_liner_base_fillet = param("bottom_liner_base_fillet", 0.6)

bottom_liner_inner_diameter = bottom_liner_outer_diameter - 2 * bottom_liner_wall_thickness
bottom_liner_inner_height = bottom_liner_height - bottom_liner_bottom_thickness

assert bottom_liner_outer_diameter < 45.0
assert abs(45.0 - bottom_liner_outer_diameter - 0.5) < 1e-6
assert abs(bottom_liner_height - 16.0) < 1e-6
assert bottom_liner_wall_thickness >= 1.2
assert bottom_liner_bottom_thickness >= 1.2
assert bottom_liner_base_fillet > 0
assert bottom_liner_base_fillet < bottom_liner_bottom_thickness

outer = Cylinder(
    bottom_liner_outer_diameter / 2,
    bottom_liner_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
bottom_edges = [e for e in outer.edges() if abs(e.center().Z) < 0.01]
if bottom_edges:
    outer = fillet(bottom_edges, radius=bottom_liner_base_fillet)

inner_cut = Pos(0, 0, bottom_liner_bottom_thickness) * Cylinder(
    bottom_liner_inner_diameter / 2,
    bottom_liner_inner_height + 0.02,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
bottom_liner = (outer - inner_cut).clean()
bottom_liner.color = srgb("#56ccf2")
print(f"bottom liner OD={bottom_liner_outer_diameter:.2f} wall={bottom_liner_wall_thickness:.2f} bottom={bottom_liner_bottom_thickness:.2f} height={bottom_liner_height:.2f}")
publish("bottom_cavity_liner", bottom_liner, "Bottom cavity liner", material="pla")
