# Copyright(c) 2019, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference('RevitAPI')
import Autodesk.Revit.DB as DB

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('System')
from System.Collections.Generic import List

view, frType, dynLoops = UnwrapElement(IN)
OUT = []
rvtLoops = List[DB.CurveLoop]()
for crvs in dynLoops:
	loop = DB.CurveLoop.Create([c.ToRevitType() for c in crvs])
	rvtLoops.Add(loop)

TransactionManager.Instance.EnsureInTransaction(doc)
fr = DB.FilledRegion.Create(doc, frType.Id, view.Id, rvtLoops)
OUT.append(fr.ToDSType(False) )
TransactionManager.Instance.TransactionTaskDone()
