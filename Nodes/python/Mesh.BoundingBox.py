# Copyright(c) 2018, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import BoundingBox, Point, Mesh

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

meshes = tolist(IN[0])
OUT = []

for m in meshes:
	if isinstance(m, Mesh):
		co = zip(*((v.X, v.Y, v.Z) for v in m.VertexPositions))
	else:
		co = zip(*((v.X, v.Y, v.Z) for v in m.Vertices()))

	OUT.append(BoundingBox.ByCorners(Point.ByCoordinates(*map(min, co)), Point.ByCoordinates(*map(max, co))))