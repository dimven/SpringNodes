import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

elements = UnwrapElement(tolist(IN[0]))
out1 = []
cut_el = []

cutU = InstanceVoidCutUtils
for i in xrange(len(elements)):
	try:
		if cutU.IsVoidInstanceCuttingElement(elements[i]):
			cut1 = cutU.GetElementsBeingCut(elements[i])
			if cut1.Count != 0:
				cut1 = [doc.GetElement(id).ToDSType(True) for id in cut1]
			out1.append(True)
			cut_el.append(cut1)
		else:
			out1.append(False)
			cut_el.append([])
	except:
		out1.append(False)
		cut_el.append([])		

OUT = out1, cut_el