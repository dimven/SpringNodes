meshes = IN[0]
vertices, indices = [], []
lastInd = 0

for m in meshes:
	vertices.extend(m.Vertices() )
	indices.extend([i + lastInd for i in m.VertexIndicesByTri()])
	lastInd += int(m.VertexCount)

OUT = m.ByVerticesAndIndices(vertices, indices)