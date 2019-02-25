#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitAPI")
import Autodesk

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

host = UnwrapElement(tolist(IN[0]))
ftype = UnwrapElement(tolist(IN[1]))
fpts = UnwrapElement(tolist(IN[2]))

OUT = []
strt = Autodesk.Revit.DB.Structure.StructuralType.NonStructural
ftp_len = len(ftype) == 1
hst_len = len(host) == 1

TransactionManager.Instance.EnsureInTransaction(doc)
for i in xrange(len(fpts) ):
	p = fpts[i].ToXyz(True)
	j = 0 if ftp_len else i
	k = 0 if hst_len else i
	try:
		if not ftype[j].IsActive : ftype[j].Activate()
		level = doc.GetElement(host[k].LevelId)
		nf = doc.Create.NewFamilyInstance(p,ftype[j],host[k],level,strt)
		OUT.append(nf.ToDSType(False))
	except:
		OUT.append(None)
TransactionManager.Instance.TransactionTaskDone()