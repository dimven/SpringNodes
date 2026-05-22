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
clr.ImportExtensions(Revit.GeometryConversion)

def singleton(x):
	if hasattr(x,'__iter__'): return x[0]
	else : return x

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]


source = UnwrapElement(singleton(IN[0]) )
dest = UnwrapElement(singleton(IN[1]) )
elements = UnwrapElement(tolist(IN[2]) )
tf1 = singleton(IN[3])

if tf1 is not None:
	tf1 = tf1.ToTransform(True)

eId = List[ElementId](e.Id for e in elements if hasattr(e, "Id") )

TransactionManager.Instance.EnsureInTransaction(doc)
copy = ElementTransformUtils.CopyElements(source, eId, dest, tf1, None)
TransactionManager.Instance.TransactionTaskDone()

OUT = [doc.GetElement(i).ToDSType(False) for i in copy]