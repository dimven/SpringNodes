#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
import clr
import System
from System.Collections.Generic import *

from itertools import repeat

pf_path = System.Environment.GetFolderPath(System.Environment.SpecialFolder.ProgramFilesX86)
import sys
sys.path.append("%s\IronPython 2.7\Lib" %pf_path)
import traceback

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

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

def PadLists(lists):
	len1 = len(lists[0])
	for i in xrange(1,len(lists)):
		len2 = len(lists[i])
		if len2 == len1 : continue
		elif len2 > len1: lists[i] = lists[i][:len1]
		else : lists[i].extend(repeat(lists[i][-1],len1 - len2))
	return lists

def NewForm(s1, isVoid1):
	message = None
	temp_path = System.IO.Path.GetTempPath()
	rand_name = System.Guid.NewGuid().ToString()
	sat_path = "%s%s.sat" % (temp_path, rand_name)
	try:
		if factor != 1:
			s1 = s1.Scale(factor)
		sat1 = Geometry.ExportToSAT(s1, sat_path)
		satOpt = SATImportOptions()
		satOpt.Placement = ImportPlacement.Origin
		satOpt.Unit = ImportUnit.Foot
		satId = doc.Import(sat1, satOpt, view1)
		opt1 = Options()
		opt1.ComputeReferences = True
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
	except:
		message = traceback.format_exc()
		pass
	if message == None:
		try:
			s2 = FreeFormElement.Create(doc,s1)
			if isVoid1:
				void_par = s2.get_Parameter(BuiltInParameter.ELEMENT_IS_CUTTING)
				void_par.Set(1)
			return s2.ToDSType(False)
		except:
			message = traceback.format_exc()
			return message
	else : return message

geom, isVoid = tolist(IN[0]),  tolist(IN[1])

acceptable_views = ("ThreeD", "FloorPlan", "EngineeringPlan", "CeilingPlan", "Elevation", "Section")
view_fec = FilteredElementCollector(doc).OfClass(View)
view1 = None
for v in view_fec:
	if str(v.ViewType) in acceptable_views and not v.IsTemplate:
		view1 = v
		break
if int(doc.Application.VersionNumber) > 2021:
	units = doc.GetUnits().GetFormatOptions(ForgeTypeId("autodesk.spec.aec:length")).GetUnitTypeId()
else:
	units = doc.GetUnits().GetFormatOptions(UnitType.UT_Length).DisplayUnits
factor = UnitUtils.ConvertToInternalUnits(1,units)
if doc.IsFamilyDocument:
	if len(geom) == len(isVoid):
		TransactionManager.Instance.EnsureInTransaction(doc)
		OUT = map(NewForm, geom, isVoid)
		TransactionManager.Instance.TransactionTaskDone()
	else:
		padded = PadLists([geom,isVoid])
		p_isVoid = padded[1]
		TransactionManager.Instance.EnsureInTransaction(doc)
		OUT = map(NewForm, geom, p_isVoid)
		TransactionManager.Instance.TransactionTaskDone()
else : OUT = "Forms can only exist in family documents"