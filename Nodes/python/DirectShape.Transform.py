#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument
app = DocumentManager.Instance.CurrentUIApplication.Application
isRvt2017 = int(app.VersionNumber) > 2016

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

units = doc.GetUnits().GetFormatOptions(UnitType.UT_Length).DisplayUnits
factor = 1 / UnitUtils.ConvertToInternalUnits(1,units)

def cs2Trans(cs, scale = factor):
	tf1 = Transform(Transform.Identity)
	tf1.Origin = cs.Origin.ToXyz(True)
	tf1.Basis[0] = cs.XAxis.ToXyz(True)
	tf1.Basis[1] = cs.YAxis.ToXyz(True)
	tf1.Basis[2] = cs.ZAxis.ToXyz(True)
	return tf1.ScaleBasis(scale)

dsTyped = UnwrapElement(IN[0])
cs1 = tolist(IN[1])

transforms = map(cs2Trans, cs1)
cat = dsTyped.Category
TypeId = dsTyped.GetTypeId()
Lib_TypeId = TypeId.ToString()
dsLib = DirectShapeLibrary.GetDirectShapeLibrary(doc)
if not dsLib.ContainsType(Lib_TypeId): dsLib.AddDefinitionType(Lib_TypeId, TypeId)

def TransformDS(transf):
	try:
		if isRvt2017:
			ds1 = DirectShape.CreateElementInstance(doc, TypeId, cat.Id, Lib_TypeId, transf)
		else:
			ds1 = DirectShape.CreateElementInstance(doc, TypeId, cat.Id, Lib_TypeId, transf, "Dynamo","spring nodes")
		ds1.SetTypeId(TypeId)
		return ds1.ToDSType(False)
	except: return None
	
TransactionManager.Instance.EnsureInTransaction(doc)
OUT = map(TransformDS, transforms)
TransactionManager.Instance.TransactionTaskDone()