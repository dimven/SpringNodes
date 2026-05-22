#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc =  DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import StructuralFramingUtils, StructuralType
FrU = StructuralFramingUtils

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

elements = UnwrapElement(tolist(IN[0]))
newloc = UnwrapElement(tolist(IN[1]))
out1 = []
framing = ("Beam", "Brace")

TransactionManager.Instance.EnsureInTransaction(doc)
for i in xrange(len(elements)):
	try:
		el_typ = elements[i].GetType().ToString()
		isWall, isBeam = False, False
		if el_typ == "Autodesk.Revit.DB.Wall":
			w_start = WallUtils.IsWallJoinAllowedAtEnd(elements[i],0)
			w_end = WallUtils.IsWallJoinAllowedAtEnd(elements[i],1)
			WallUtils.DisallowWallJoinAtEnd(elements[i],0)
			WallUtils.DisallowWallJoinAtEnd(elements[i],1)
			isWall = True
		elif el_typ == "Autodesk.Revit.DB.FamilyInstance":
			if elements[i].StructuralType.ToString() in framing:
				b_start = FrU.IsJoinAllowedAtEnd(elements[i],0)
				b_end = FrU.IsJoinAllowedAtEnd(elements[i],1)
				FrU.DisallowJoinAtEnd(elements[i],0)
				FrU.DisallowJoinAtEnd(elements[i],1)
				isBeam = True	
		newloc1 = newloc[i].ToRevitType()
		oldloc = elements[i].Location
		loc_typ = oldloc.GetType().ToString()
		if loc_typ == "Autodesk.Revit.DB.LocationCurve":
			oldloc.Curve = newloc1
		elif loc_typ == "Autodesk.Revit.DB.LocationPoint":
			oldloc.Point = newloc1
		if isWall:
			if w_start: WallUtils.AllowWallJoinAtEnd(elements[i],0)
			if w_end: WallUtils.AllowWallJoinAtEnd(elements[i],1)
		if isBeam:
			if b_start: FrU.AllowJoinAtEnd(elements[i],0)
			if b_end: FrU.AllowJoinAtEnd(elements[i],1)
		out1.append(elements[i].ToDSType(True))
	except:
		out1.append(None)
TransactionManager.Instance.TransactionTaskDone()

OUT = out1