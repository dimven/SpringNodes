#Copyright(c) 2015, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ElementId
from Autodesk.Revit.DB.Structure import StructuralFramingUtils

clr.AddReference("System")
from System.Collections.Generic import List as cList

def tolist(obj1):
	if hasattr(obj1,"__iter__"):
		return obj1
	else:
		return [obj1]

beams = UnwrapElement(tolist(IN[0]))

TransactionManager.Instance.EnsureInTransaction(doc)
for b in beams:
	try:
		StructuralFramingUtils.DisallowJoinAtEnd(b,0)
		StructuralFramingUtils.DisallowJoinAtEnd(b,1)
	except:
		pass
		
ids1 = [e.Id for e in beams]
ids2 = cList[ElementId](ids1)
uidoc.Selection.SetElementIds(ids2)
OUT = "%s beams corrected in Revit." %ids2.Count
TransactionManager.Instance.TransactionTaskDone()