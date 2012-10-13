import math

class Base(object) :
	@classmethod
	def format(cls, v) :
		# I am far too sleepy to be programming this
		try :
			exp = math.floor(math.log10(v))
		except ValueError :
			exp = 0

		factor = math.pow(10, exp)
		sig = v / factor

		pref = '%0.6f' % sig

		sign = {
			True  : '+',
			False : '-'
		}[exp >= 0]

		suf = 'e%s%02d' % (sign, abs(exp))

		return pref + suf

# TODO lazy-evaluate the serialization to string/text.  Right now, if you modify the positions of anything after creation it won't serialize right.

class Point(Base) :
	def __init__(self, x, y, z) :
		self.x = x
		self.xf = Base.format(x)
		self.y = y
		self.yf = Base.format(y)
		self.z = z
		self.zf = Base.format(z)
		self.pf = "%s %s %s" % (self.xf, self.yf, self.zf)
		Base.__init__(self)

class Triangle(Base) :
	def __init__(self, p1, p2, p3) :
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.tf = """facet normal 0.00000000e+0 0.00000000e+0 0.00000000e+0
outer loop
vertex %s
vertex %s
vertex %s
endloop
endfacet
""" % (self.p1.pf, self.p2.pf, self.p3.pf)

class Solid(Base) :
	def __init__(self, name) :
		self.name = name
		self.triangles = list()

	def add(self, triangle) :
		self.triangles.append(triangle)

	def write(self, fh) :
		fh.write("solid %s\n" % self.name)
		for triangle in self.triangles :
			fh.write(triangle.tf)
		fh.write("endsolid %s\n" % self.name)

def serialize_to_file(solids, fh) :
	for solid in solids :
		solid.write(fh)

def serialize(solids, f) :
	if isinstance(f, basestring) :
		fh = open(f, 'w')
		try :
			serialize_to_file(solids, fh)
		finally :
			fh.close()
	else :
		fh = f
		serialize_to_file(solids, fh)
