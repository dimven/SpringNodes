import clr

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('RevitAPI')
import Autodesk.Revit.DB as DB

from System.Collections.Generic import List

indices = List[int]()
def toTkMesh(m, indices=indices, N=range(3)):
	verts = (v.ToPoint(1) for v in m.Vertices)
	indices.Clear()
	for i in xrange(m.NumTriangles):
		for j in N:
			indices.Add(m.Triangle[i].Index[j])
	
	return mtk.Mesh.ByVerticesAndIndices(verts, indices)

elems, tessFactor, asTkMesh = UnwrapElement(IN)
OUT = []
opt1 = DB.Options()

if asTkMesh:
	clr.AddReference('MeshToolkit')
	import Autodesk.Dynamo.MeshToolkit as mtk

def getMeshGeo(rvtGeo, geoList=None, opt1=opt1):
	if geoList is None:
		geoList = []
	for g in rvtGeo:
		if isinstance(g, DB.GeometryInstance):
			getMeshGeo(g.GetInstanceGeometry(), geoList)
		elif isinstance(g, DB.Mesh):
			geoList.append(g)
		elif isinstance(g, DB.Face):
			geoList.append(g.Triangulate(tessFactor))
		elif isinstance(g, DB.Solid):
			vol = getattr(g, 'Volume', 0)
			if vol > 0:
				geoList.extend(f.Triangulate(tessFactor) for f in g.Faces)
	return geoList

for e in elems:
	meshGeo = getMeshGeo(e.Geometry[opt1])
	if asTkMesh:
		OUT.append(map(toTkMesh, meshGeo))
	else:
		OUT.append([m.Convert() for m in meshGeo])
opt1.Dispose()