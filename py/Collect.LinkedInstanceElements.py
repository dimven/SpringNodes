# Copyright(c) 2018, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, RevitLinkType, ElementMulticategoryFilter, ElementId

from System.Collections.Generic import List

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

links = UnwrapElement(tolist(IN[0]) )
cats = UnwrapElement(tolist(IN[1]) )
elements, transforms = [], []
OUT = elements, transforms

ueWrapper = None
wrappers = clr.GetClrType(Revit.Elements.ElementWrapper).GetMethods()
for w in wrappers:
	if w.ToString().startswith("Revit.Elements.UnknownElement"):
		ueWrapper = w
		break

for link in links:
	try:
		if RevitLinkType.IsLoaded(doc, link.GetTypeId() ):
			linkDoc = link.GetLinkDocument()
			catId = List[ElementId](c.Id for c in cats)
			catFil = ElementMulticategoryFilter(catId)
			fec = FilteredElementCollector(linkDoc).WhereElementIsNotElementType().WherePasses(catFil)
			linkEls = []
			for e in fec:
				try:
					linkEls.append(e.ToDSType(True) )
				except:
					if ueWrapper:
						linkEls.append(ueWrapper.Invoke(None, (e, True) ) )
			elements.append(linkEls)
			transforms.append(link.GetTotalTransform().ToCoordinateSystem(1) )
			fec.Dispose()
			catFil.Dispose()
		else:
			elements.append('Linked document is unloaded')
			transforms.append(None)
	except Exception, ex:
		elements.append(str(ex) )
		transforms.append(None)