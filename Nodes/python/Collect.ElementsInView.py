# Copyright(c) 2018, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, ElementMulticategoryFilter, ElementId

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

from System.Collections.Generic import List

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

views = UnwrapElement(tolist(IN[0]) )
cat = UnwrapElement(IN[1])
OUT = []

ueWrapper = None
wrappers = clr.GetClrType(Revit.Elements.ElementWrapper).GetMethods()
for w in wrappers:
	if w.ToString().startswith("Revit.Elements.UnknownElement"):
		ueWrapper = w
		break

if cat is not None:
	catId = List[ElementId]()
	for c in tolist(cat):
		catId.Add(c.Id)
	catFil = ElementMulticategoryFilter(catId)
else:
	catFil = None

for v in views:
	fec = FilteredElementCollector(doc, v.Id).WhereElementIsNotElementType()
	if catFil is not None:
		fec = fec.WherePasses(catFil)
	viewEl = []
	for e in fec:
		try:
			viewEl.append(e.ToDSType(True) )
		except:
			if ueWrapper:
				viewEl.append(ueWrapper.Invoke(None, (e, True) ) )
	OUT.append(viewEl)
	fec.Dispose()
if catFil is not None:
	catFil.Dispose()