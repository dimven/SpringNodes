# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

famtypes = UnwrapElement(tolist(IN[0]) )
newnames = tolist(IN[1])

OUT = []
fec = FilteredElementCollector(doc).OfClass(famtypes[0].GetType() )
type_dict = dict([(Element.Name.__get__(i), i) for i in fec])

ft_len = len(famtypes) == 1
TransactionManager.Instance.EnsureInTransaction(doc)
for i in xrange(len(newnames) ):
	j = 0 if ft_len else i
	n1 = str(newnames[i])
	if n1 in type_dict:
		OUT.append(type_dict[n1].ToDSType(False) ) #do I want to wrap this?
	else:
		try:
			nt1 = famtypes[j].Duplicate(n1)
			type_dict[n1] = nt1
			OUT.append(nt1.ToDSType(True) )
		except:
			OUT.append(None)
TransactionManager.Instance.TransactionTaskDone()