import stereololography as stl
import stereololography.projection as proj
import math

stl.Point.unit = stl.cm

p1 = stl.Point(0.0, 0.0, 0.0)
p2 = stl.Point(1.0, 0.0, 0.0)
p3 = stl.Point(0.5, 1.0, 0.0)
p4 = stl.Point(0.5, 0.5, 1.0)
triangle1 = stl.Triangle(p1, p2, p3)
triangle2 = stl.Triangle(p1, p2, p4)
triangle3 = stl.Triangle(p1, p4, p3)
triangle4 = stl.Triangle(p4, p2, p3)
solid = stl.Solid("default")
solid.add(triangle1)
solid.add(triangle2)
solid.add(triangle3)
solid.add(triangle4)
stl.serialize([solid], "tetra-almost.stl")

# guesstimated inputs.
# How do tait-bryan angles relate to the camera point?

for x in [2,3,4,5,6] :
	p = proj.Projector(stl.Point(x, 3.8, 4.2), (math.pi * -1/16,math.pi * 1/8.0, 0))
	layer = p.project(solid)
	layer.write('tetra-almost-x%0.3f.svg' % (float(x)))
