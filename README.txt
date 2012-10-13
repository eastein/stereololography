# LOL, STL

STL is an okay format but want to code my 3D prints! Make me triangles! Fly, my pretties!

# OK, so how do I make an STL?

It's easy! Just go like:

    import stereololography as stl
    p1 = stl.Point(0.2, 0.1, 0.8)
    p2 = stl.Point(0.2, 0.8, 0.2)
    p3 = stl.Point(0.8, 0.1, 0.2)
    triangle = stl.Triangle(p1, p2, p3)
    solid = stl.Solid("default")
    solid.add(triangle)
    stl.serialize([solid], "out.stl")

This will work with either a filehandle or a string filename. If you supply a string filename, it will be opened for writing, truncate mode, and closed when the function completes. This will happen even if the file was not fully written due to an error. Nothing will be deleted on error.
