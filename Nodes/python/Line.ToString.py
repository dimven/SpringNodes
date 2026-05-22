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
def p2s(p, sep, digits):
	x = n2s(p.X, digits)
	y = n2s(p.Y, digits)
	z = n2s(p.Z, digits)
	return ''.join( (x, sep, y, sep, z) )
	
def l2s(l, sep=IN[1], digits=IN[2]):
	a = p2s(l.StartPoint, sep, digits)
	b = p2s(l.EndPoint, sep, digits)
	return ''.join( (a, sep, b) )

lines = tolist(IN[0])

OUT = map(l2s, lines)