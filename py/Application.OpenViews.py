import clr

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

OUT = [doc.GetElement(v.ViewId).ToDSType(1) for v in uidoc.GetOpenUIViews()]