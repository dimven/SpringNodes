import System
import clr
clr.AddReference('RevitAPI')
import Autodesk.Revit.DB as DB

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

from System.Collections.Generic import List

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

x = UnwrapElement(tolist(IN[0]))

fec = DB.FilteredElementCollector(doc).WhereElementIsNotElementType()
if isinstance(x[0], DB.Category):
	catId = List[DB.ElementId](c.Id for c in x)
	filter = DB.ElementMulticategoryFilter(catId)
	
elif isinstance(x[0], DB.ElementType):
	types = List[System.Type](t.GetType() for t in x)
	filter = DB.ElementMulticlassFilter(types)
else:
	types = List[System.Type](x)
	filter = DB.ElementMulticlassFilter(types)

fec.WherePasses(filter)
OUT = [e.ToDSType(1) for e in fec]
fec.Dispose()
filter.Dispose()