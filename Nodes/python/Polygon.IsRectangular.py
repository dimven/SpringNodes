# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

from itertools import imap

def tolist(obj1):
	if hasattr(obj1,'__iter__'): return obj1
	else: return [obj1]

def isSq(pts):
	def _dist(a, b):
		return round( (a.X - b.X)**2 + (a.Y - b.Y)**2  + (a.Z - b.Z)**2, 5)
	isSquare, isRect = False, False
	ln1 = len(pts)
	if len(pts) != 4:
		return isSquare, isRect, isSquare ^ isRect
	a, b, c, d = pts
	ab, ac, bc, bd = map(_dist, (a,a,b,b), (b,c,c,d) )
	if ac == bd:
		isSquare = ab == bc
		isRect = True if isSquare else ab == _dist(c, d)
	return isSquare, isRect, isSquare ^ isRect

def getPts(p):
	return p.Points if 'Polygon' in p.GetType().ToString() else [c.StartPoint for c in p.Curves()]

polys = tolist(IN[0])
OUT = zip(*map(isSq, imap(getPts, polys) ) )