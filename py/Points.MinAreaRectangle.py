import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Point, Vector, Rectangle
from math import sqrt
from operator import itemgetter

_pts, elev = IN

def hull(_pts):
	def pCrs(o, a, b):
		return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

	pts = sorted( (p.X, p.Y) for p in _pts)
	pLen = len(pts)
	if pLen < 4 : return pts
	else:
		lower, upper = [], []
		
		for i in xrange(pLen):
			j = pLen - 1 - i
			while len(lower) >= 2 and pCrs(lower[-2], lower[-1], pts[i]) <= 0.000001:
				lower.pop()
			lower.append(pts[i])
			while len(upper) >= 2 and pCrs(upper[-2], upper[-1], pts[j]) <= 0.000001:
				upper.pop()
			upper.append(pts[j])
		
		lower.pop()
		upper.pop()
		lower.extend(upper)
		return lower

# http://eprints.cs.vt.edu/archive/00000869/01/CS81017-R.pdf

def scalar(k, i, j):
	return k[0] * (i[1] - j[1]) + k[1] * (j[0] - i[0]) + j[1] * i[0] - i[1] * j[0]

def pDist(a, b, sqrt=sqrt):
	return sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2)

def linDist(a, b, p):
	line_dist = pDist(a, b)
	if line_dist == 0:
		return a, pDist(p, a)
	
	t = ( (p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1]) ) / line_dist**2
	
	cp = ( (b[0] - a[0]) * t + a[0], (b[1] - a[1]) * t + a[1])
	d1 = pDist(p, cp)
	return cp, d1

def indexer(end, position=0, start=0, step=1):
	i = position - step
	while True:
		i += step
		if i >= end:
			i = start
		yield i

def highSearch(pts, iPt, jPt, j, it1=None, k=None, m=None,
			   indexer=indexer, scalar=scalar):
	if it1 is None:
		it1 = indexer(len(pts), j)
		k, m = it1.next(), it1.next()
	Sa = scalar(pts[k], iPt, jPt)
	Sb = scalar(pts[m], iPt, jPt)
	while Sa < Sb:
		k, m = m, it1.next()
		Sa = scalar(pts[k], iPt, jPt)
		Sb = scalar(pts[m], iPt, jPt)
	return k, m

pts = hull(_pts)

OUT = []
highPts, closePts, areas, dists = [], [], [], []
lnPts = len(pts)

it1 = indexer(lnPts, 2)
k, m = it1.next(), it1.next()

for i in xrange(lnPts):
	j = (i + 1) % lnPts

	k, m = highSearch(pts, pts[i], pts[j], j+1, it1, k, m)
	
	highPts.append(pts[k])
	cp, l1 = linDist(pts[i], pts[j], pts[k])
	closePts.append(cp)
	
	n, _ = highSearch(pts, pts[k], cp, j)
	_, l2a = linDist(pts[k], cp, pts[n])
		
	q, _ = highSearch(pts, cp, pts[k], m)
	_, l2b = linDist(cp, pts[k], pts[q])
	
	areas.append(l1 * (l2a + l2b) )
	dists.append( (l2a, l2b) )

ix, _ = min(enumerate(areas), key=itemgetter(1) )
d1, d2 = dists[ix]
_a, _b = closePts[ix], highPts[ix]
a = Point.ByCoordinates(_a[0], _a[1], elev)
b = Point.ByCoordinates(_b[0], _b[1], elev)

_v = Vector.ByTwoPoints(a, b)
v = Vector.ByCoordinates(-_v.Y, _v.X, 0).Normalized()
p1 = a.Add(v.Scale(d2) )
p2 = a.Subtract(v.Scale(d1) )
p3 = b.Subtract(v.Scale(d1) )
p4 = b.Add(v.Scale(d2) )

OUT = (Rectangle.ByCornerPoints(p1, p2, p3, p4), 
90 - v.AngleAboutAxis(Vector.XAxis(), Vector.ZAxis() ),
[Point.ByCoordinates(p[0], p[1], elev) for p in pts])