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

dsTyped, vecs = UnwrapElement(IN[0]), tolist(IN[1])

transforms = []
for i in xrange(len(vecs)):
	try: transforms.append(Transform.CreateTranslation(vecs[i].ToXyz(True)))
	except: pass
cat = dsTyped.Category
TypeId = dsTyped.GetTypeId()
Lib_TypeId = TypeId.ToString()
dsLib = DirectShapeLibrary.GetDirectShapeLibrary(doc)
if not dsLib.ContainsType(Lib_TypeId): dsLib.AddDefinitionType(Lib_TypeId, TypeId)

def CopyDS(transf):
	try:
		if isRvt2017:
			ds1 = DirectShape.CreateElementInstance(doc, TypeId, cat.Id, Lib_TypeId, transf)
		else:
			ds1 = DirectShape.CreateElementInstance(doc, TypeId, cat.Id, Lib_TypeId, transf, "Dynamo","spring nodes")
		ds1.SetTypeId(TypeId)
		return ds1.ToDSType(False)
	except: return None
	
TransactionManager.Instance.EnsureInTransaction(doc)
OUT = map(CopyDS, transforms)
TransactionManager.Instance.TransactionTaskDone()