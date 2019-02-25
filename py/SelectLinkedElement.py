# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import RevitLinkInstance, Transform 

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

sel1 = uidoc.Selection
ot1 = Selection.ObjectType.Element
ot2 = Selection.ObjectType.LinkedElement
li_ref = sel1.PickObject(ot1, "Select a link instance first.")
link1 = doc.GetElement(li_ref.ElementId)
if isinstance(link1, RevitLinkInstance):
	el_ref = sel1.PickObject(ot2, "Pick a linked element.")
	LinkDoc = link1.GetLinkDocument()
	tf1 = link1.GetTotalTransform().ToCoordinateSystem(True)
	OUT = LinkDoc.GetElement(el_ref.LinkedElementId).ToDSType(True), tf1
else:
	OUT = link1, Transform.Identity.ToCoordinateSystem(True)