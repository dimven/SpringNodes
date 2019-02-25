#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

def output1(l1):
	if len(l1) == 1: return l1[0]
	else: return l1

selid = uidoc.Selection.GetElementIds()
OUT = output1([doc.GetElement(id).ToDSType(True) for id in selid])