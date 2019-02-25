#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr
import math

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

elements = UnwrapElement(tolist(IN[0]))
getModel = IN[1]

accepted_mc = "Autodesk.Revit.DB.ModelLine, Autodesk.Revit.DB.ModelArc, Autodesk.Revit.DB.ModelEllipse, Autodesk.Revit.DB.ModelHermiteSpline, Autodesk.Revit.DB.ModelNurbSpline"

def almost_eq(line, mc):
	line2 = mc.Location.Curve
	xyz1 = line.Evaluate(0.5, True)
	if not line2.IsBound:
		xyz2 = line2.Center
		try: xyz1 = line.Center
		except: pass
	else:
		xyz2 = line2.Evaluate(0.5, True)
	if xyz1.DistanceTo(xyz2) <= 0.0001:
		return True
	else:
		return False

def clean1(l1):
	for i in xrange(len(l1) ):
		l1[i] = [x for x in l1[i] if x != None]
	return l1

def getSketch(el1):
	try:
		sk1 = doc.GetElement(ElementId(el1.Id.IntegerValue - 1) )
	except:
		sk1 = None
	if not getModel and sk1 is not None and sk1.GetType().ToString() == 'Autodesk.Revit.DB.Sketch':
		profile = sk1.Profile
	else:
		t1 = SubTransaction(doc)
		t1.Start()
		deleted = doc.Delete(el1.Id)
		t1.RollBack()
		
		profile, mc = CurveArrArray(), []
		for d in deleted:
			test_el = doc.GetElement(d)
			el_type = test_el.GetType().ToString()
			if el_type == "Autodesk.Revit.DB.Sketch":
				profile = test_el.Profile
				if not getModel:
					break
			elif getModel and el_type in accepted_mc :
				mc.append(test_el)

	ordered_mc = [ [None] * i.Size for i in profile] if getModel else []
	curves = [ [None] * i.Size for i in profile]
	for i in xrange(profile.Size):
		for j in xrange(profile[i].Size):
			curves[i][j] = profile[i][j].ToProtoType()
			if getModel:
				for k in xrange(len(mc)):
					if almost_eq(profile[i][j], mc[k]):
						ordered_mc[i][j] = mc[k].ToDSType(True)
						del mc[k]
						break
						
	return curves, clean1(ordered_mc)

TransactionManager.Instance.EnsureInTransaction(doc)
result = map(getSketch, elements)
TransactionManager.Instance.TransactionTaskDone()
OUT = [r[0] for r in result], [r[1] for r in result]