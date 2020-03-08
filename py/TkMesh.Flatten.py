# Copyright(c) 2020, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry as DS

meshes, Z = IN

OUT = []
for m in meshes:
	vertices = [DS.Point.ByCoordinates(p.X, p.Y, Z) for p in m.Vertices()]
	indices = m.VertexIndicesByTri()
	OUT.append(m.ByVerticesAndIndices(vertices, indices))