# cell: top_cavity_liner
# Removable liner for one top-lid chamber.
from build123d import *

top_liner_outer_diameter = param("top_liner_outer_diameter", 44.5)
top_liner_height = param("top_liner_height", 16.0)
top_liner_wall_thickness = param("top_liner_wall_thickness", 1.3)
top_liner_bottom_thickness = param("top_liner_bottom_thickness", 1.7)
top_liner_base_fillet = param("top_liner_base_fillet", 0.6)

top_liner_inner_diameter = top_liner_outer_diameter - 2 * top_liner_wall_thickness
top_liner_inner_height = top_liner_height - top_liner_bottom_thickness

assert top_liner_outer_diameter < 45.0
assert abs(45.0 - top_liner_outer_diameter - 0.5) < 1e-6
assert abs(top_liner_height - 16.0) < 1e-6
assert top_liner_wall_thickness >= 1.2
assert top_liner_bottom_thickness >= 1.2
assert top_liner_base_fillet > 0
assert top_liner_base_fillet < top_liner_bottom_thickness

outer = Cylinder(
    top_liner_outer_diameter / 2,
    top_liner_height,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
bottom_edges = [e for e in outer.edges() if abs(e.center().Z) < 0.01]
if bottom_edges:
    outer = fillet(bottom_edges, radius=top_liner_base_fillet)

inner_cut = Pos(0, 0, top_liner_bottom_thickness) * Cylinder(
    top_liner_inner_diameter / 2,
    top_liner_inner_height + 0.02,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
top_liner = (outer - inner_cut).clean()
top_liner.color = srgb("#f2c94c")
print(f"top liner OD={top_liner_outer_diameter:.2f} wall={top_liner_wall_thickness:.2f} bottom={top_liner_bottom_thickness:.2f} height={top_liner_height:.2f}")
publish("top_cavity_liner", top_liner, "Top cavity liner", material="pla")
