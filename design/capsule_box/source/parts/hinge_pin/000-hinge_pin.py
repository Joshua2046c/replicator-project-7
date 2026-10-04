# Cut-stock hinge pin for the compact three-knuckle hinge
from build123d import *

hinge_pin_diameter = param("hinge_pin_diameter", 3.0)
hinge_pin_length = param("hinge_pin_length", 29.41)  # revised compact pin length

pin = Cylinder(
    hinge_pin_diameter / 2,
    hinge_pin_length,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)
publish("hinge_pin", pin, "Metal hinge pin")
