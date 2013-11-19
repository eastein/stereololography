import tornado.web
import tornado.ioloop
import tornado.httpclient


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

# How do tait-bryan angles relate to the camera point?

def render(x, y, z, a1, a2, a3) :
	p = proj.Projector(stl.Point(x, y, z), (a1, a2, a3))
	layer = p.project(solid).slice_lines()
	return layer.render()

class BaseHandler(tornado.web.RequestHandler):
	def wj(self, status, j) :
		self.application.__io_instance__.add_callback(lambda: self._wj(status, j))

	def _wj(self, status, j) :
		self.set_status(status)
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Cache-Control', 'no-cache')
		self.set_header('Content-Type', 'image/svg+xml')
		self.write(j)
		self.finish()


class Render(BaseHandler):
	@tornado.web.asynchronous
	def get(self, x, y, z, a1, a2, a3) :
		self._wj(200, render(float(x), float(y), float(z), float(a1), float(a2), float(a3)))


handler_set = [
	(r"/render/([\-]{0,1}[0-9]+\.[0-9]+),([\-]{0,1}[0-9]+\.[0-9]+),([\-]{0,1}[0-9]+\.[0-9]+)/([\-]{0,1}[0-9]+\.[0-9]+),([\-]{0,1}[0-9]+\.[0-9]+),([\-]{0,1}[0-9]+\.[0-9]+)$", Render),
]

application = tornado.web.Application(handler_set)

application.listen(8088)

application.__io_instance__ = tornado.ioloop.IOLoop.instance()
application.__io_instance__.start()
