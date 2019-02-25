# Copyright(c) 2018, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import ElementId

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

inv = ElementId.InvalidElementId

items = tolist(IN[0])
param = IN[1]
OUT = []

TransactionManager.Instance.EnsureInTransaction(doc)
for i in items:
	itm = None
	par = i.InternalElement.LookupParameter(param)
	if par is not None:
		try:
			par.Set(inv)
			itm = i
		except:
			pass
	OUT.append(itm)
TransactionManager.Instance.TransactionTaskDone()