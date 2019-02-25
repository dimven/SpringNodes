# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import RevitLinkInstance

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
	el_ref = sel1.PickObjects(ot2, "Select the linked elements and press Finish.")
	linkDoc = link1.GetLinkDocument()
	Lel_id = [r1.LinkedElementId for r1 in el_ref]
	tf1 = link1.GetTotalTransform().ToCoordinateSystem(True)
	OUT = [linkDoc.GetElement(id1).ToDSType(True) for id1 in Lel_id], tf1
else:
	OUT = "Failed to pick a linked instance", None