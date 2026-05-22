# Copyright(c) 2019, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
import System
from itertools import repeat

pf_path = System.Environment.GetFolderPath(System.Environment.SpecialFolder.ProgramFilesX86)
import sys
sys.path.append("%s\IronPython 2.7\Lib" %pf_path)
import traceback

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as RVT

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

def PadLists(lists):
	len1 = len(lists[0])
	for i in xrange(1,len(lists)):
		len2 = len(lists[i])
		if len2 == len1 : continue
		elif len2 > len1: lists[i] = lists[i][:len1]
		else : lists[i].extend(repeat(lists[i][-1],len1 - len2))
	return lists

def NewDS_R17(geom1, cat1, name1, mat1): 
	toDispose = []
	try:
		edg_enum = dict()
		br1 = RVT.BRepBuilder(RVT.BRepType.OpenShell)
		toDispose.append(br1)
		for f in geom1.Faces:
			s1 = f.SurfaceGeometry()
			toDispose.append(s1)
			planarTest = Curve.ByParameterLineOnSurface(s1, UV.ByCoordinates(0.01,0.0), UV.ByCoordinates(0.99,1))
			isPlanar = abs(planarTest.StartPoint.DistanceTo(planarTest.EndPoint) - planarTest.Length) <= 0.00001
			toDispose.append(planarTest)
			if isPlanar:
				o1 = s1.PointAtParameter(0.5,0.5).ToXyz(True)
				v1 = s1.NormalAtParameter(0.5,0.5).ToXyz(True)
				sf1 = RVT.BRepBuilderSurfaceGeometry.Create(RVT.Plane.CreateByNormalAndOrigin(v1, o1), None)
				isFlipped = False
			else:
				ns1 = s1.ToNurbsSurface()
				toDispose.append(ns1)
				isFlipped = s1.NormalAtParameter(0.5, 0.5).Dot(ns1.NormalAtParameter(0.5, 0.5) ) < 0
				pts1 = [j.ToXyz(True) for i in ns1.ControlPoints() for j in i ]
				weights = [j for i in ns1.Weights() for j in i]
				sf1 = RVT.BRepBuilderSurfaceGeometry.CreateNURBSSurface(
					ns1.DegreeU,ns1.DegreeV, ns1.UKnots(), ns1.VKnots(), pts1, weights, False, None)
			toDispose.append(sf1)
			sfId = br1.AddFace(sf1, isFlipped)
			if mat1 is not None:
				br1.SetFaceMaterialId(sfId, mat1.Id)
			for lp in f.Loops:
				lp1 = br1.AddLoop(sfId)
				for ce in lp.CoEdges:
					edg = ce.Edge
					c0 = edg.CurveGeometry
					toDispose.append(c0)
					mp = c0.PointAtParameter(0.5)
					toDispose.append(mp)
					edgHash = (round(mp.X, 5), round(mp.Y, 5), round(mp.Z, 5))
					eId, isReversed, ceCount = edg_enum.get(edgHash, [None, None, None])
					if eId is None:
						try:
							c1 = c0.ToRevitType(True)
						except:
							n = len(c0.ToNurbsCurve().ControlPoints() )
							pts = [c0.PointAtParameter(1.0/n * j) for j in xrange(n + 1)]
							toDispose.extend(pts)
							c1 = NurbsCurve.ByPoints(pts).ToRevitType(True)
						toDispose.append(c1)
						e1 = RVT.BRepBuilderEdgeGeometry.Create(c1)
						toDispose.append(e1)
						eId = br1.AddEdge(e1)
						isReversed = ce.Reversed
						ceCount = 0
						edg_enum[edgHash] = [eId, not isReversed, ceCount]
					if ceCount <= 1:
						br1.AddCoEdge(lp1, eId, isReversed)
						edg_enum[edgHash][-1] += 1
			br1.FinishLoop(lp1)
			br1.FinishFace(sfId)
		result = br1.Finish()
		if result == RVT.BRepBuilderOutcome.Success:
			if cat1 is None or not RVT.DirectShape.IsValidCategoryId(cat1.Id, doc):
				cat1Id = RVT.ElementId(RVT.BuiltInCategory.OST_GenericModel)
			else:
				cat1Id = cat1.Id
			if name1 in dst_enum: #definition exists
				old_type = dst_enum[name1]
				old_type.SetShape(br1)
				fec1 = RVT.FilteredElementCollector(doc).OfClass(RVT.DirectShape).WhereElementIsNotElementType()
				insts = [i for i in fec1 if i.GetTypeId().Equals(old_type.Id)]
				if insts:
					ds1 = insts[0]
				else:
					dsLib.AddDefinitionType(name1, old_type.Id)
					ds1 = RVT.DirectShape.CreateElementInstance(doc, old_type.Id, cat1Id, name1, tf1)
					ds1.SetTypeId(old_type.Id)
			else:
				dsType1 = RVT.DirectShapeType.Create(doc, name1, cat1Id)
				dsType1.SetShape(br1)
				dsLib.AddDefinitionType(name1, dsType1.Id)
				ds1 = RVT.DirectShape.CreateElementInstance(doc, dsType1.Id, cat1Id, name1, tf1)
				ds1.SetTypeId(dsType1.Id)
			
			return ueWrapper.Invoke(None, (ds1, False) )
		else:
			return result
	except:
		return traceback.format_exc()
	finally:
		for i in toDispose: i.Dispose()

solids = tolist(IN[0])
cat = tolist(IN[1])
cat = [UnwrapElement(c) for c in cat]
names = tolist(IN[2])
mat = tolist(IN[3])
mat = [UnwrapElement(m) for m in mat]

dsLib = RVT.DirectShapeLibrary.GetDirectShapeLibrary(doc)
tf1 = RVT.Transform.Identity

dst_fec = RVT.FilteredElementCollector(doc).OfClass(RVT.DirectShapeType)
dst_enum = dict([(RVT.Element.Name.__get__(i), i) for i in dst_fec])

ueWrapper = None
wrappers = clr.GetClrType(Revit.Elements.ElementWrapper).GetMethods()
for w in wrappers:
	if w.ToString().startswith("Revit.Elements.UnknownElement"):
		ueWrapper = w
		break

if len(solids) == len(names):
	if not len(solids) == len(cat) == len(mat):
		padded = PadLists([solids, cat, mat])
		cat, mat = padded[1:]
	TransactionManager.Instance.EnsureInTransaction(doc)
	OUT = map(NewDS_R17, solids, cat, names, mat)
	TransactionManager.Instance.TransactionTaskDone()
else : OUT = "Make sure that each geometry\nobject has a unique type name."