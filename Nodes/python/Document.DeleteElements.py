#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

elems = UnwrapElement(tolist(IN[0]) )

if IN[1]:
	deleted, failed = [], []
	TransactionManager.Instance.EnsureInTransaction(doc)
	for e in elems:
		id = None
		try:
			id = e.Id
			del_id = doc.Delete(id)
			deleted.extend([d.ToString() for d in del_id])
		except:
			if id is not None:
				failed.append(id.ToString() )
	TransactionManager.Instance.TransactionTaskDone()
	s = set(deleted)
	failed1 = [x for x in failed if x not in s]
	OUT = len(deleted), ';'.join(deleted), ';'.join(failed1)
else:
	OUT = "Set confirm to True", "", ""