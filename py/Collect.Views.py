#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

fn = map(str,tolist(IN[0]) )
IncSchedules = IN[1]
result, similar, names = [], [], []

if IncSchedules: exclude = ("DrawingSheet")
else: exclude = ("DrawingSheet", "Schedule")
fec = FilteredElementCollector(doc).OfClass(View)
for i in fec:
	if not i.IsTemplate and not i.ViewType.ToString() in exclude:
		n1 = i.ViewName
		names.append(n1)
		if any(fn1 == n1 for fn1 in fn):
			result.append(i.ToDSType(True))
		elif any(fn1.lower() in n1.lower() for fn1 in fn):
			similar.append(i.ToDSType(True))
if len(result) > 0:
	OUT = result,similar
if len(result) == 0 and len(similar) > 0:
	OUT = "No exact match found. Check partial below:", similar
if len(result) == 0 and len(similar) == 0:
	OUT = "No match found! Check names below:", names