# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

def n2s(n, digits=IN[1]):
	if digits is not None:
		n = round(n, digits)
	n = unicode(n)
	if n.endswith('.0'):
		n = n[:-2]
	return n

OUT = map(n2s, tolist(IN[0]))