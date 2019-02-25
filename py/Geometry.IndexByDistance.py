# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

from operator import lt, gt
from sys import maxsize

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

geom = tolist(IN[0])
other = tolist(IN[1])
isClosest = IN[2]

_fn = lt if isClosest else gt
_base = maxsize if isClosest else -maxsize
inds, dists = [], []
OUT = inds, dists

for g in geom:
	d = _base
	ind, i = 0, 0
	for o in other:
		d1 = g.DistanceTo(o)
		if _fn(d1, d):
			d = d1
			ind = i
		i += 1
	inds.append(ind)
	dists.append(d)