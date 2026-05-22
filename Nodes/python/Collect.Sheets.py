#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
app = DocumentManager.Instance.CurrentUIApplication.Application
isRvt2018 = int(app.VersionNumber) < 2019

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

fn = map(str,tolist(IN[0]) )
NameNumber = IN[1]
result, similar, names = [], [], []

fec = FilteredElementCollector(doc).OfClass(View)
ds_type = "DrawingSheet"
for i in fec:
	if i.ViewType.ToString() == ds_type:
		if NameNumber: n1 = i.ViewName if isRvt2018 else i.Name
		else: n1 = i.SheetNumber
		names.append(n1)
		if any(fn1 == n1 for fn1 in fn):
			result.append(i.ToDSType(True))
		elif any(fn1.lower() in n1.lower() for fn1 in fn):
			similar.append(i.ToDSType(True))
if len(result) > 0:
	OUT = result,similar
if len(result) == 0 and len(similar) > 0:
	OUT = "No exact match found. Check partial below:",similar
if len(result) == 0 and len(similar) == 0:
	OUT = "No match found! Check values below:", names