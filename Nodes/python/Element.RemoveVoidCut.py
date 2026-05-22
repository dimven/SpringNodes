# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

def singleton(x):
	if hasattr(x,'__iter__'): return x[0]
	else : return x

elem = UnwrapElement(singleton(IN[0]) )
cuts = UnwrapElement(tolist(IN[1]) )
out1 = []

cutU = InstanceVoidCutUtils
OUT = 0
if cutU.CanBeCutWithVoid(elem):
	TransactionManager.Instance.EnsureInTransaction(doc)
	for c in cuts:
		if cutU.IsVoidInstanceCuttingElement(c) and \
		cutU.InstanceVoidCutExists(elem, c):
			try:
				cutU.RemoveInstanceVoidCut(doc,ToBeCut[i],Cuts[j])
				OUT += 1
			except:
				pass
	TransactionManager.Instance.TransactionTaskDone()