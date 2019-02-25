# Copyright(c) 2018, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference("RevitAPI")
#from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import FamilyInstanceCreationData
from Autodesk.Revit.DB.Structure import StructuralType

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("System")
from System.Collections.Generic import List

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

pts, types, lvls, _track = map(tolist, UnwrapElement(IN))
trackElems = not _track[0]
types_len = len(types) == 1
lvl_len = len(lvls) == 1

st1 = StructuralType.NonStructural
FICD1 = List[FamilyInstanceCreationData]()
for i, p in enumerate(pts):
	t1 = types[0] if types_len else types[i]
	lvl = lvls[0] if lvl_len else lvls[i]
	FICD1.Add(FamilyInstanceCreationData(p.ToXyz(True), t1, lvl, st1) )

TransactionManager.Instance.EnsureInTransaction(doc)
new_inst = doc.Create.NewFamilyInstances2(FICD1)
TransactionManager.Instance.TransactionTaskDone()

OUT = [doc.GetElement(i).ToDSType(trackElems) for i in new_inst]