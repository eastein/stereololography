import stereololography as stl

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
stl.serialize([solid], "out.stl")
