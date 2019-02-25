#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

#inspired by Troy Gates https://forums.autodesk.com/t5/revit-api/revit-api-selected-element-set-order/td-p/5597203

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

def output1(l1):
	if len(l1) == 1: return l1[0]
	else: return l1

sel1 = uidoc.Selection
obt1 = Selection.ObjectType.Element
msg1 = 'Pick elements in the desired order, hit ESC to stop picking.'
out1 = []

flag = True
TaskDialog.Show("Spring Nodes", msg1)
while flag:
	try:
		el1 = doc.GetElement(sel1.PickObject(obt1, msg1).ElementId)
		out1.append(el1.ToDSType(True))
	except : flag = False

OUT = output1(out1)