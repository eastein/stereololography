import svgcuts
import math
import stereololography as stl

# am I using left handed vs right handed axes? I think my projection code is for left handed, but it's entirely possible the axes used in stereololography are right handed.
class Projector(object) :
	"""
	@param c the camera point
	@param t the camera orientation; x,y,z (tait-bryan angles).
	@param e the viewer's position relative to the display surface.
	"""
	def __init__(self, c, t) :
		self.c = c
		self.t = t
		# position has to be messed around. It doesn't work quite right sense so far.
		self.e = (0.0,0.0,2.0)

	# TODO add a parameter for how large a viewport to use, and what units. Add support to svgcuts to use all the units stereololography supports
	# TODO add an option to automatically home the camera? should it work by translating and scaling the render after it's done, or adjusting the 
	# theta parameters to the visible portions of the scene?
	def project(self, o) :
		# TODO don't default the size and units of the layer.
		layer = svgcuts.Layer(8.0, 6.0, unit="in")
		
		self.project_inner(layer, o)

		# TODO move this to example? or parameterize it somehow. Either way, this is important for getting your bearings on how the
		# coordinate system is laid out.
		
		n = 2
		r = 0.1
		m = .8
		for x in range(-n, n + 1) :
			for y in range(-n, n + 1) :
				for z in range(-n, n + 1) :
					if x == 0 and y == 0 and z == 0 :
						continue

					c = r * m
					_c = math.pow(math.pow(x, 2.0) + math.pow(y, 2.0) + math.pow(z, 2.0), 0.5)
					xm = x / _c * c
					ym = y / _c * c
					zm = z / _c * c
					p1 = stl.Point(x * m, y * m, z * m)
					p2 = stl.Point(x * m + xm, y * m + ym, z * m + zm)

					p1 = self.project_point(p1)
					p2 = self.project_point(p2)

					# axes colors
					kw = {}
					if y == 0 and z == 0 :
						kw['color'] = 'red'
					elif x == 0 and z == 0 :
						kw['color'] = 'green'
					elif x == 0 and y == 0 :
						kw['color'] = 'blue'

					layer.add_line(svgcuts.Line(p1, p2, **kw))
		return layer

	def project_inner(self, l, o) :
		# TODO determine mechanic to use for edge hiding; add a trait/property to triangles for visibility of the edges (not just a bool)
		if isinstance(o, list) :
			for o_ in o :
				self.project_inner(l, o_)
		elif isinstance(o, stl.Solid) :
			for t in o.triangles :
				self.project_inner(l, t)
		elif isinstance(o, stl.Triangle) :
			p1 = self.project_point(o.p1)
			p2 = self.project_point(o.p2)
			p3 = self.project_point(o.p3)
			l.add_line(svgcuts.Line(p1, p2, unit='in'))
			l.add_line(svgcuts.Line(p1, p3, unit='in'))
			l.add_line(svgcuts.Line(p2, p3, unit='in'))

	"""
	@param a the point to project into 2d space
	"""
	def project_point(self, a) :
		print 'projecting a point: %s' % a.pf
		# this goes from a stereololography point to an svgcuts point.
		# all stl points are already in millimeters.

		# math taken from the wikipedia page on 3d perspective projection
		dx = math.cos(self.t[1]) * (math.sin(self.t[2]) * (a.y - self.c.y) + math.cos(self.t[2]) * (a.x - self.c.x)) - math.sin(self.t[1]) * (a.z - self.c.z)
		dy = math.sin(self.t[0]) * (math.cos(self.t[1]) * (a.z - self.c.z) + math.sin(self.t[1]) * (math.sin(self.t[2]) * (a.y - self.c.y) + math.cos(self.t[2]) * (a.x - self.c.x))) + math.cos(self.t[0]) * (math.cos(self.t[2]) * (a.y - self.c.y) - math.sin(self.t[2]) * (a.x - self.c.x))

		dz = math.cos(self.t[0]) * (math.cos(self.t[1]) * (a.z - self.c.z) + math.sin(self.t[1]) * (math.sin(self.t[2]) * (a.y - self.c.y) + math.cos(self.t[2]) * (a.x - self.c.x))) - math.sin(self.t[0]) * (math.cos(self.t[2]) * (a.y - self.c.y) - math.sin(self.t[2]) * (a.x - self.c.x))

		print 'd: <%f, %f, %f>' % (dx, dy, dz)

		ex = self.e[0]
		ey = self.e[1]
		ez = self.e[2]

		bx = (dx - ex) * (ez/dz)
		by = (dy - ey) * (ez/dz)

		print 'b: <%f, %f>' % (bx, by)

		return svgcuts.Point(bx, by)
