# Cut-stock hinge pin made from plain metal rod
from build123d import *

hinge_pin_diameter = param("hinge_pin_diameter", 3.0)
hinge_pin_length = param("hinge_pin_length", 61.0)

pin = Cylinder(
    hinge_pin_diameter / 2,
    hinge_pin_length,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)
publish("hinge_pin", pin, "Metal hinge pin")
