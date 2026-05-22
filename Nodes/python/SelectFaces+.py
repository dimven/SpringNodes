#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitAPIUI")
from  Autodesk.Revit.UI import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

def output1(x):
	if len(x) == 1: return x[0]
	else : return x

surfaces, gpoints = [], []
sel1 = uidoc.Selection
ot1 = Selection.ObjectType.Face
ref_list = sel1.PickObjects(ot1, "Select the faces and press Finish.")
for ref in ref_list:
	el1 = doc.GetElement(ref.ElementId)
	sf0 = el1.GetGeometryObjectFromReference(ref)
	if isinstance(el1, FamilyInstance):
		tf1 = el1.GetTransform().ToCoordinateSystem()
		sf1 = sf0.Convert(ref, tf1)
	else:
		sf1 = sf0.ToProtoType(True)
	for i in sf1: i.Tags.AddTag("RevitFaceReference", ref)
	surfaces.append(output1(sf1) )
	gpoints.append(ref.GlobalPoint.ToPoint(True) )

OUT = output1(surfaces), output1(gpoints)