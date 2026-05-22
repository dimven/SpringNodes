# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net
from math import sqrt
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Vector, Point, Mesh

from itertools import izip_longest

def tolist(obj1):
	if hasattr(obj1,'__iter__'): return obj1
	return [obj1]

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def tkMeshData(m):
	vol, area = 0, 0
	tris = grouper(m.TrianglesAsNineNumbers, 9)
	for t in tris:
		a, b, c = (Vector.ByCoordinates(*c) for c in grouper(t, 3))
		e1 = b - a
		e2 = c - a
		N = e1.Cross(e2)
		area += 0.5 * N.Length
		f = a.X + b.X + c.X
		vol += N.X * f
		for i in a, b, c, e1, e2, N:
			i.Dispose()
	return vol / 6.0, area

def meshData(m):
	vol, area = 0, 0
	vp = m.VertexPositions
	ptslist = ([vp[i.A], vp[i.B], vp[i.C]] for i in m.FaceIndices)
	for pts in ptslist:
		a, b, c = map(Point.AsVector, pts)
		e1 = b - a
		e2 = c - a
		N = e1.Cross(e2)
		area += 0.5 * N.Length
		f = a.X + b.X + c.X
		vol += N.X * f
		for i in a, b, c, e1, e2, N:
			i.Dispose()
	return vol / 6.0, area

meshes = tolist(IN[0])
volumes, areas = [], []
OUT = volumes, areas
for m in meshes:
	f = meshData if isinstance(m, Mesh) else tkMeshData
	v, a = f(m)
	volumes.append(v)
	areas.append(a)