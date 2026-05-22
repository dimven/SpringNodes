import clr

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

OUT = None
if doc.IsWorkshared:
	cp = doc.GetWorksharingCentralModelPath()
	OUT = ModelPathUtils.ConvertModelPathToUserVisiblePath(cp)