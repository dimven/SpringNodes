# Copyright(c) 2019, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import Selection

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
ot = Selection.ObjectType.LinkedElement
el_ref = sel1.PickObject(ot, "Pick a linked element.")
linkInst = doc.GetElement(el_ref.ElementId)
linkDoc = linkInst.GetLinkDocument()
linkEl = linkDoc.GetElement(el_ref.LinkedElementId).ToDSType(1)
tf1 = linkInst.GetTotalTransform().ToCoordinateSystem(1)
OUT = linkEl, tf1