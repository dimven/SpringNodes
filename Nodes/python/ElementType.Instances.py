import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

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

types = UnwrapElement(tolist(IN[0]) )
catNames = set()
for t in types:
	c1 = t.Category
	if c1 is not None:
		catNames.add(c1.Name)

catId = List[ElementId]()
allCats = doc.Settings.Categories
for cn in catNames:
	if allCats.Contains(cn):
		catId.Add(allCats[cn].Id)

type_storage = dict()
fec = FilteredElementCollector(doc).WhereElementIsNotElementType()
if catId:
	fec = fec.WherePasses(ElementMulticategoryFilter(catId) )

for e in fec:
	id1 = e.GetTypeId().IntegerValue
	if id1 in type_storage:
		type_storage[id1].append(e.ToDSType(True) )
	else:
		type_storage[id1] = [e.ToDSType(True)]

OUT = [type_storage.get(t.Id.IntegerValue, None) for t in types]