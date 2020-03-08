import clr

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitAPI')
import Autodesk.Revit.DB as DB

def tolist(x):
    if hasattr(x,'__iter__'): return x
    return [x]

links = tolist(UnwrapElement(IN[0]))
OUT = [DB.RevitLinkType.IsLoaded(doc, x.Id) for x in links]