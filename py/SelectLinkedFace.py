# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

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

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import RevitLinkInstance, FamilyInstance

def output1(x):
	if len(x) == 1: return x[0]
	else : return x

sel1 = uidoc.Selection
ot1 = Selection.ObjectType.Element
ot2 = Selection.ObjectType.PointOnElement
li_ref = sel1.PickObject(ot1, "Select a link instance first.")
link1 = doc.GetElement(li_ref.ElementId)
if isinstance(link1, RevitLinkInstance):
	tf1 = link1.GetTotalTransform()
	face_ref = sel1.PickObject(ot2, "Pick a face.")
	linkDoc = link1.GetLinkDocument()
	el1 = linkDoc.GetElement(face_ref.LinkedElementId)
	face_ref2 = face_ref.CreateReferenceInLink()
	sf0 = el1.GetGeometryObjectFromReference(face_ref2)
	if isinstance(el1, FamilyInstance):
		tf1 *= el1.GetTotalTransform()
	sf1 = sf0.Convert(face_ref2, tf1.ToCoordinateSystem(True) )
	for s in sf1:	
		s.Tags.AddTag("RevitFaceReference", face_ref)
	OUT = output1(sf1), face_ref.GlobalPoint.ToPoint(True)
else:
	OUT = "Failed to pick a link instance.", None