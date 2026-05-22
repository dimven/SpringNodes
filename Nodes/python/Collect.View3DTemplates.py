import clr

clr.AddReference('RevitAPI')
import Autodesk.Revit.DB as DB

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

ueWrapper = None
wrappers = clr.GetClrType(Revit.Elements.ElementWrapper).GetMethods()
for w in wrappers:
	if w.ToString().startswith("Revit.Elements.UnknownElement"):
		ueWrapper = w
		break

fec = DB.FilteredElementCollector(doc).OfClass(DB.View3D)
OUT = []
for i in fec:
	if i.IsTemplate:
		OUT.append(ueWrapper.Invoke(None, (i, True) ))