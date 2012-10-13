<A name="toc1-0" title="LOL, STL" />
# LOL, STL

STL is an okay format but want to code my 3D prints! Make me triangles! Fly, my pretties!

<A name="toc1-5" title="OK, so how do I make an STL?" />
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

<A name="toc1-21" title="Example" />
# Example

The first working case (example_tetra-almost.py) is shown having results here: https://twitter.com/toba/status/257051666371710976

    python example_tetra-almost.py

Load this into your favorite 3D printing setup and you're off to the races.  For makerbot Replicator:

* load into ReplicatorG
* click create gcode
* choose a print-head
* set the correct filament size
* go for it
* create SD card image, copy outputted file onto SD card
* put in printer
* print from SD card
