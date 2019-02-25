#Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
import System
import sys
from System.Collections.Generic import *

from itertools import repeat

pf_path = System.Environment.GetFolderPath(System.Environment.SpecialFolder.ProgramFilesX86)
sys.path.append("%s\IronPython 2.7\Lib" %pf_path)
import traceback

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument
app = DocumentManager.Instance.CurrentUIApplication.Application
isRvt2017 = int(app.VersionNumber) > 2016

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as RVT

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

def PadLists(lists):
	len1 = len(lists[0])
	for i in xrange(1,len(lists)):
		len2 = len(lists[i])
		if len2 == len1 : continue
		elif len2 > len1: lists[i] = lists[i][:len1]
		else : lists[i].extend(repeat(lists[i][-1],len1 - len2))
	return lists

def NewDS(s1, cat1, name1):
	temp_path = System.IO.Path.GetTempPath()
	sat_path = "%s%s.sat"% (temp_path, name1)
	try:
		if factor != 1:
			s1 = s1.Scale(factor)
		sat1 = Geometry.ExportToSAT(s1, sat_path)
		satId = doc.Import(sat1, satOpt, view1)
		el1 = doc.GetElement(satId)
		geom1 = el1.get_Geometry(opt1)
		enum = geom1.GetEnumerator()
		enum.MoveNext()
		geom2 = enum.Current.GetInstanceGeometry()
		enum2 = geom2.GetEnumerator()
		enum2.MoveNext()
		s1 = enum2.Current
		doc.Delete(satId)
		System.IO.File.Delete(sat_path)
		
		if cat1 is None or not RVT.DirectShape.IsValidCategoryId(cat1.Id, doc):
			cat1Id = RVT.ElementId(RVT.BuiltInCategory.OST_GenericModel)
		else:
			cat1Id = cat1.Id

		if name1 in dst_enum:
			old_type = dst_enum[name1]
			old_type.SetShape([s1])
			fec1 = RVT.FilteredElementCollector(doc).OfClass(RVT.DirectShape).WhereElementIsNotElementType()
			insts = [i for i in fec1 if i.GetTypeId().Equals(old_type.Id)]
			if insts:
				ds1 = insts[0]
			else:
				dsLib.AddDefinitionType(name1, old_type.Id)
				if isRvt2017:
					ds1 = RVT.DirectShape.CreateElementInstance(doc, old_type.Id, cat1Id, name1, tf1)
				else:
					ds1 = RVT.DirectShape.CreateElementInstance(doc, old_type.Id, cat1Id, name1, tf1, "Dynamo", "spring nodes")
				ds1.SetTypeId(old_type.Id)
		else:
			dsType1 = RVT.DirectShapeType.Create(doc, name1, cat1Id)
			dsType1.SetShape([s1])
			dsLib.AddDefinitionType(name1, dsType1.Id)
			dst_enum[name1] = dsType1
			if isRvt2017:
				ds1 = RVT.DirectShape.CreateElementInstance(doc, dsType1.Id, cat1Id, name1, tf1)
			else:
				ds1 = RVT.DirectShape.CreateElementInstance(doc, dsType1.Id, cat1Id, name1, tf1, "Dynamo", "spring nodes")
			ds1.SetTypeId(dsType1.Id)

		return ueWrapper.Invoke(None, (ds1, False) )
	except:
		return traceback.format_exc()

solids = tolist(IN[0])
cat = map(UnwrapElement, tolist(IN[1]) )
names = tolist(IN[2])

satOpt = RVT.SATImportOptions()
satOpt.Placement = RVT.ImportPlacement.Origin
satOpt.Unit = RVT.ImportUnit.Foot
opt1 = RVT.Options()
opt1.ComputeReferences = True

acceptable_views = "ThreeD, FloorPlan, EngineeringPlan, CeilingPlan, Elevation, Section"
view_fec = RVT.FilteredElementCollector(doc).OfClass(RVT.View)
view1 = None
for v in view_fec:
	if v.ViewType.ToString() in acceptable_views and not v.IsTemplate:
		view1 = v
		break

units = doc.GetUnits().GetFormatOptions(RVT.UnitType.UT_Length).DisplayUnits
factor = RVT.UnitUtils.ConvertToInternalUnits(1, units)

dsLib = RVT.DirectShapeLibrary.GetDirectShapeLibrary(doc)
tf1 = RVT.Transform.Identity

dst_fec = RVT.FilteredElementCollector(doc).OfClass(RVT.DirectShapeType)
dst_enum = dict( (RVT.Element.Name.__get__(i), i) for i in dst_fec)

ueWrapper = None
wrappers = clr.GetClrType(Revit.Elements.ElementWrapper).GetMethods()
for w in wrappers:
	if w.ToString().startswith("Revit.Elements.UnknownElement"):
		ueWrapper = w
		break

if len(solids) == len(names):
	if not len(solids) == len(cat):
		padded = PadLists( (solids, cat) )
		cat = padded[1]
	TransactionManager.Instance.EnsureInTransaction(doc)
	OUT = map(NewDS, solids, cat, names)
	TransactionManager.Instance.TransactionTaskDone()
else :
	OUT = "Make sure that each geometry\nobject has a unique type name."
satOpt.Dispose()
opt1.Dispose()