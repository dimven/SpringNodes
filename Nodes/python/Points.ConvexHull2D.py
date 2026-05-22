import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Point

from itertools import chain

pts = sorted( (p.X, p.Y) for p in IN[0])
elev = IN[1]

def pCrs(o, a, b):
	return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

pLen = len(pts)
if pLen < 4 : OUT = pts
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
	
	OUT = [Point.ByCoordinates(p[0], p[1], elev) for p in chain(lower, upper) ]