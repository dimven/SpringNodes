# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

#inspired by Troy Gates https://forums.autodesk.com/t5/revit-api/revit-api-selected-element-set-order/td-p/5597203

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
obt1 = Selection.ObjectType.Element
obt2 = Selection.ObjectType.LinkedElement
picked = []

if IN[0]:
	TaskDialog.Show("Spring Nodes", "First select a link instance. Then pick elements from that instance in the desired order. Hit ESC to stop picking.")

msg1 = 'Pick elements in the desired order, hit ESC to stop picking.'

li_ref = sel1.PickObject(obt1, "Select a link instance first.")
link1 = doc.GetElement(li_ref.ElementId)
if isinstance(link1, RevitLinkInstance):
	linkDoc = link1.GetLinkDocument()
	
	flag = True
	while flag:
		try:
			el1 = sel1.PickObject(obt2, msg1).LinkedElementId
			if el1.IntegerValue != -1:
				picked.append(el1)
		except : flag = False
	
	elems = []
	for p in picked:
		el1 = linkDoc.GetElement(p)
		if el1 is not None:
			elems.append(el1.ToDSType(True) )
	
	tf1 = link1.GetTotalTransform().ToCoordinateSystem(True)
	OUT = elems, tf1
	
else:
	OUT = 'Failed to pick a link instance', None