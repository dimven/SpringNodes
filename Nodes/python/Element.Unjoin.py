# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

def singleton(x):
	if hasattr(x,'__iter__'): return x[0]
	else : return x

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

floor = UnwrapElement(singleton(IN[0]) )
beams = UnwrapElement(tolist(IN[1]) )

OUT = 0
TransactionManager.Instance.EnsureInTransaction(doc)
for b in beams:
	if JoinGeometryUtils.AreElementsJoined(doc, floor, b):
		JoinGeometryUtils.UnjoinGeometry(doc, floor, b)
		OUT += 1
TransactionManager.Instance.TransactionTaskDone()