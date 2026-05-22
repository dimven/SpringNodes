# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

def n2s(n, digits):
	if digits is not None:
		n = round(n, digits)
	s1 = str(n)
	if s1[-2:] == '.0':
		s1 = s1[:-2]
	return s1
def p2s(p, sep=IN[1], digits=IN[2]):
	x = n2s(p.X, digits)
	y = n2s(p.Y, digits)
	z = n2s(p.Z, digits)
	return ''.join( (x, sep, y, sep, z) )

pts = tolist(IN[0])

OUT = map(p2s, pts)