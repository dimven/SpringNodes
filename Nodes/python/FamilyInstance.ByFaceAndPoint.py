# Copyright(c) 2018, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('RevitAPI')
import Autodesk.Revit.DB as DB

def tolist(x):
	if hasattr(x,'__iter__'): return x
	return [x]

def first(x):
	if hasattr(x,'__iter__'): return x[0]
	return x

host = first(IN[0])
ftype = UnwrapElement(tolist(IN[1]))
pts = tolist(IN[2])

OUT = []
ftp_len = len(ftype) == 1
ref1 = host.Tags.LookupTag("RevitFaceReference")

TransactionManager.Instance.EnsureInTransaction(doc)
for i, p in enumerate(pts):
	j = 0 if ftp_len else i
	if not ftype[j].IsActive:
		ftype[j].Activate()
	faceNor = host.NormalAtPoint(p)
	up = Vector.ZAxis()
	if abs(faceNor.Dot(up)) > 0.9999: #is horizontal
		#uv1 = host.UVParameterAtPoint(p)
		#dir1 = host.TangentAtUParameter(uv1.U,uv1.V).ToXyz()
		dir1 = DB.XYZ.BasisX
	else:
		dir1 = faceNor.Cross(up).ToXyz()
	try:
		inst1 = doc.Create.NewFamilyInstance(ref1, p.ToXyz(1), dir1, ftype[j])
		OUT.append(inst1.ToDSType(False) )
	except Exception as ex: OUT.append(str(ex))
TransactionManager.Instance.TransactionTaskDone()