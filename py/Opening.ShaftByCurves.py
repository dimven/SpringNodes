#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc =  DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

hole = UnwrapElement(IN[0])
base_lvl = UnwrapElement(tolist(IN[1]))
top_lvl = UnwrapElement(tolist(IN[2]))

openings = []
newhl = []

if not any(hasattr(h,"__iter__") for h in hole):
	hole = [hole]
TransactionManager.Instance.EnsureInTransaction(doc)
for i in xrange(len(hole)):
	z = CurveArray()
	[z.Append(j.ToRevitType()) for j in hole[i] ]
	newhl.append(z)
if len(base_lvl) == 1 and len(top_lvl) == 1 :
	for i in xrange(len(newhl)):
		try:
			x = doc.Create.NewOpening(base_lvl[0], top_lvl[0], newhl[i])
			openings.append(x.ToDSType(False))
		except:
			openings.append(None)
else:
	for h, b, t in zip(newhl, base_lvl, top_lvl):
		try:
			x = doc.Create.NewOpening(b, t, h)
			openings.append(x.ToDSType(False))
		except:
			openings.append(None)
TransactionManager.Instance.TransactionTaskDone()

OUT = openings