import clr

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

from System.Collections.Generic import List

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

def singleton(x):
	if hasattr(x,'__iter__'): return x[0]
	else : return x

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]


linkInst = UnwrapElement(singleton(IN[0]) )
elements = UnwrapElement(tolist(IN[1]) )

linkDoc = linkInst.GetLinkDocument()
tf1 = linkInst.GetTotalTransform()
eId = List[ElementId]()
for e in elements:
	try:
		id1 = e.Id
	except:
		continue
	eId.Add(id1)

TransactionManager.Instance.EnsureInTransaction(doc)
copy = ElementTransformUtils.CopyElements(linkDoc, eId, doc, tf1, None)
TransactionManager.Instance.TransactionTaskDone()
OUT = []
for i in copy:
	e = doc.GetElement(i)
	if e is not None:
		OUT.append(e.ToDSType(False))