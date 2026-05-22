# Copyright(c) 2020, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry as DS

from itertools import izip_longest
def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

meshes, vecs, dists = IN

def getMeshPerimeter(mesh):
	edge_dict = {}
	indices = list(mesh.VertexIndicesByTri())
	tris = grouper(indices, 3)
	for t in tris:
		a, b, c = t
		sides = frozenset((a, b)), frozenset((b, c)), frozenset((c, a))
		for s in sides:
			edge_dict[s] = edge_dict.get(s, 0) + 1
	
	perim = [e for e, n in edge_dict.iteritems() if n == 1]
	return perim

def thickenMesh(mesh, vec, dist):
	vertices = list(mesh.Vertices())
	indices = list(mesh.VertexIndicesByTri())
	n = len(vertices)
	topMesh = mesh.Translate(vec, dist)
	vertices.extend(topMesh.Vertices())
	indices.extend([i + n for i in topMesh.VertexIndicesByTri()])

	for e in getMeshPerimeter(mesh):
		a, b = e
		c, d = a + n, b + n
		indices.extend([a, b, c])
		indices.extend([c, d, b])

	return mesh.ByVerticesAndIndices(vertices, indices)

singleVec = len(vecs) == 1
singleDist = len(dists) == 1
OUT = []
for i in xrange(len(meshes)):
	j = 0 if singleVec else i
	k = 0 if singleDist else i
	OUT.append(thickenMesh(meshes[i], vecs[j], dists[k]))
