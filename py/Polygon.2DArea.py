# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

def tolist(obj1):
	if hasattr(obj1,'__iter__'): return obj1
	else: return [obj1]

#https://stackoverflow.com/questions/2432428/is-there-any-algorithm-for-calculating-area-of-a-shape-given-co-ordinates-that-d

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
	a = 0
	l1 = len(pts)
	for i in xrange(l1):
		j = i + 1
		if j == l1:
			j = 0
		a += pts[i].X * pts[j].Y
		a -=  pts[i].Y * pts[j].X
	OUT.append(abs(a/2.0) )