#Copyright(c) 2015, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
#code inspired by Harry Mattison
#https://boostyourbim.wordpress.com

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

def tolist(obj1):
	if hasattr(obj1,"__iter__") : return obj1
	else : return [obj1]

def first(obj1):
	if hasattr(obj1,'__iter__') : return obj1[0]
	else : return obj1

views = UnwrapElement(tolist(IN[0]))
name1 = str(first(IN[1]) )
overwrite = IN[2]
vs_exists = None

fec = FilteredElementCollector(doc).OfClass(ViewSheetSet).GetElementIterator()
fec.Reset()
for f in fec:
	if f.Name == name1:
		vs_exists = f
		break
if vs_exists != None and overwrite:
	TransactionManager.Instance.EnsureInTransaction(doc)
	doc.Delete(vs_exists.Id)
	TransactionManager.Instance.TransactionTaskDone()
	vs_exists = None
elif vs_exists != None and not overwrite:
	OUT = "There's a ViewSet with the same name.\nSet Overwrite to true to continue."
if vs_exists == None:
	vs1 = ViewSet()
	for v in views: (vs1.Insert(v))
	printMan = doc.PrintManager
	printMan.PrintRange = PrintRange.Select
	viewSS = printMan.ViewSheetSetting
	try:
		TransactionManager.Instance.EnsureInTransaction(doc)
		viewSS.CurrentViewSheetSet.Views = vs1
		viewSS.SaveAs(name1)
		TransactionManager.Instance.TransactionTaskDone()
		OUT = "ViewSet created with %s views inside." %len(views)
	except:
		OUT = "The ViewSet could not be created"