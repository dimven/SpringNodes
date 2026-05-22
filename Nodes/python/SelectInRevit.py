#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
#inspired by Julien Benoit @jbenoit44 
#http://aecuandme.wordpress.com/

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ElementId
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI.Selection import *

clr.AddReference("System")
from System.Collections.Generic import List as cList

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

elements = UnwrapElement(tolist(IN[0]) )
ids1 = []
for i in xrange(len(elements)):
	try:(ids1.append(elements[i].Id))
	except: pass
ids2 = cList[ElementId](ids1)
uidoc.Selection.SetElementIds(ids2)
OUT = "%s elements selected in Revit." %ids2.Count