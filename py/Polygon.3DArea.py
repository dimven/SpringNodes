# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net
from math import sqrt
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Vector

def tolist(obj1):
	if hasattr(obj1,'__iter__'): return obj1
	else: return [obj1]

polys = tolist(IN[0])
OUT = []
for p in polys:
	t1 = p.GetType().ToString()
	if 'Polygon' in t1 or 'Rectangle' in t1:
		pts = p.Points
	elif 'PolyCurve' in t1:
		pts = [c.StartPoint for c in p.Curves()]
	else:
		area.append(None)
		continue
	total = Vector.ByCoordinates(0,0,0)
	vec = [p.AsVector() for p in pts]
	l1 = len(pts)
	for i in xrange(l1):
		j = i + 1
		if j == l1:
			j = 0
		prod = vec[i].Cross(vec[j])
		total = total.Add(prod)
	OUT.append(abs(sqrt(total.Dot(total) ) / 2.0) )