# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

def tolist(obj1):
	if hasattr(obj1,'__iter__'): return obj1
	else: return [obj1]

def containment(poly, pt):
	def testCCW(A,B,C): return (B.X - A.X) * (C.Y - A.Y) > (B.Y - A.Y) * (C.X - A.X)
	
	wn = 0
	ln1 = len(poly)
	for i in xrange(ln1):
		j = (i+1) % ln1
		isCCW = testCCW(poly[i], poly[j], pt)
		if poly[i].Y <= pt.Y:
			if poly[j].Y > pt.Y and isCCW: wn += 1
		else:
			if poly[j].Y <= pt.Y and not isCCW: wn -= 1
	
	return wn != 0

poly = IN[0]
pts = tolist(IN[1])
t1 = poly.GetType().ToString()
if 'Polygon' in t1 or 'Rectangle' in t1:
	poly_pts = poly.Points
else:
	poly_pts = [c.StartPoint for c in poly.Curves()]

OUT = [containment(poly_pts, p) for p in pts]