# Copyright(c) 2018, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitAPI')
import Autodesk.Revit.DB as DB

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

view = UnwrapElement(tolist(IN[0]))
pts = tolist(IN[1])
content = map(str, tolist(IN[2]))
txtType = UnwrapElement(tolist(IN[3]))
_txtAlign = str(IN[4])
persistent = not IN[5]

txtAlign_dict = {"Center" : DB.HorizontalTextAlignment.Center,
				 "Left"   : DB.HorizontalTextAlignment.Left,
				 "Right"  : DB.HorizontalTextAlignment.Right}
txtAlign = txtAlign_dict.get(_txtAlign, None)
if txtAlign is None:
	txtAlign = txtAlign_dict["Center"]

if txtType[0] is None:
	txtType[0] = doc.GetElement(doc.GetDefaultElementTypeId(DB.ElementTypeGroup.TextNoteType))

OUT = []
txtType_len = len(txtType) == 1
view_len = len(view) == 1
content_len = len(content) == 1

TransactionManager.Instance.EnsureInTransaction(doc)
for i in xrange(len(pts) ):
	p = pts[i].ToXyz(True)
	j = 0 if txtType_len else i
	k = 0 if view_len else i
	m = 0 if content_len else i
	try:
		tn = DB.TextNote.Create(doc, view[k].Id, p, content[m], txtType[j].Id)
		tn.HorizontalAlignment = txtAlign
		OUT.append(tn.ToDSType(persistent) )
	except:
		OUT.append(None)
TransactionManager.Instance.TransactionTaskDone()