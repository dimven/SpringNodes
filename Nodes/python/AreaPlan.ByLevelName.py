import clr

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

def tolist(obj1):
	if hasattr(obj1,'__iter__') : return obj1
	else : return [obj1]

def first(obj1):
	if hasattr(obj1,'__iter__'): return obj1[0]
	else: return obj1

	
lvls = UnwrapElement(tolist(IN[0]) )
names = tolist(IN[1])
plan_type = str(first(IN[2]) )

#fail_str = 'view with same name exists'
vt1 = None # fetch the area plan type
fec1 = FilteredElementCollector(doc).OfClass(ViewFamilyType)
for f in fec1:
	if Element.Name.__get__(f) == plan_type :
		vt1 = f.Id
		break

fec2 = FilteredElementCollector(doc).OfClass(View) #get existing area plans
plan_names = [f.Name for f in fec2 if f.GetTypeId().Equals(vt1)]

as1 = None #get the scheme
fec3 = FilteredElementCollector(doc).OfClass(AreaScheme)
for f in fec3:
	if f.Name == plan_type :
		as1 = f.Id
		break

if as1 != None:
	OUT = []
	TransactionManager.Instance.EnsureInTransaction(doc)
	for l, n in zip(lvls, names):
		if n not in plan_names:
			v1 = ViewPlan.CreateAreaPlan(doc, as1, l.Id)
			v1.Name = n
			OUT.append(v1.ToDSType(False) )
		else : OUT.append(None) #could use fail_str but filtering nulls is easier
	TransactionManager.Instance.TransactionTaskDone()

else : OUT = 'Area scheme with that name not found.'