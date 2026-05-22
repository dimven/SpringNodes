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
cutters = []

cutU = InstanceVoidCutUtils
for i in xrange(len(elements)):
	try:
		if cutU.CanBeCutWithVoid(elements[i]):
			cut1 = cutU.GetCuttingVoidInstances(elements[i])
			if cut1.Count == 0:
				out1.append(False)
				cutters.append([])
			else:
				out1.append(True)
				cut1 = [doc.GetElement(id).ToDSType(True) for id in cut1]
				cutters.append(cut1)
		else:
			out1.append(False)
			cutters.append([])
	except:
		out1.append(False)
		cutters.append([])		

OUT = out1, cutters