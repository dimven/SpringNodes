#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr
import System
from System.Collections.Generic import *

from itertools import repeat

pf_path = System.Environment.GetFolderPath(System.Environment.SpecialFolder.ProgramFilesX86)
import sys
sys.path.append('%s\IronPython 2.7\Lib' %pf_path)
import traceback

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
from Autodesk.DesignScript.Geometry import Point as DynPoint

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import StructuralType

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

def tolist(obj1):
	if hasattr(obj1,'__iter__'): return obj1
	else: return [obj1]

def PadLists(lists):
	len1 = len(lists[0])
	for i in xrange(1,len(lists)):
		len2 = len(lists[i])
		if len2 == len1 : continue
		elif len2 > len1: lists[i] = lists[i][:len1]
		else : lists[i].extend(repeat(lists[i][-1],len1 - len2))
	return lists

class FamOpt1(IFamilyLoadOptions):
	def __init__(self):
		pass
	def OnFamilyFound(self,familyInUse, overwriteParameterValues):
		return True
	def OnSharedFamilyFound(self,familyInUse, source, overwriteParameterValues):
		return True

geom = tolist(IN[0])
fam_path = IN[1]
names = tolist(IN[2])
category = tolist(IN[3])
material = tolist(IN[4])
isVoid = tolist(IN[5])
subcat = tolist(IN[6])

units = doc.GetUnits().GetFormatOptions(UnitType.UT_Length).DisplayUnits
factor = UnitUtils.ConvertToInternalUnits(1,units)
acceptable_views = ('ThreeD', 'FloorPlan', 'EngineeringPlan', 'CeilingPlan', 'Elevation', 'Section')
origin = XYZ.Zero
str_typ = StructuralType.NonStructural
t1 = TransactionManager.Instance
temp_path = System.IO.Path.GetTempPath()
invalid_chars = System.IO.Path.GetInvalidFileNameChars()
satOpt = SATImportOptions()
satOpt.Placement = ImportPlacement.Origin
satOpt.Unit = ImportUnit.Foot
opt1 = Options()
opt1.ComputeReferences = True
SaveAsOpt = SaveAsOptions()
SaveAsOpt.OverwriteExistingFile = True

def NewForm_background(s1, name1, cat1, isVoid1, mat1, subcat1):
	try:
		enable_mat = False if mat1 is None else True
		enable_subcat = False if subcat1 is None else True
		if any( (c in name1 for c in invalid_chars) ):
			raise Exception('Family name contains invalid characters')
		TransactionManager.ForceCloseTransaction(t1)
		famdoc = doc.Application.NewFamilyDocument(fam_path)
		sat_path = '%s%s.sat' % (temp_path, name1)
		if factor != 1:
			s1 = s1.Scale(factor)
		vec1 = Vector.ByTwoPoints(BoundingBox.ByGeometry(s1).MinPoint, DynPoint.Origin())
		s1 = s1.Translate(vec1)
		sat1 = Geometry.ExportToSAT(s1, sat_path)
		view_fec = FilteredElementCollector(famdoc).OfClass(View)
		view1 = None
		for v in view_fec:
			if str(v.ViewType) in acceptable_views and not v.IsTemplate:
				view1 = v
				break
		t1.EnsureInTransaction(famdoc)
		satId = famdoc.Import(sat1, satOpt, view1)
		el1 = famdoc.GetElement(satId)
		geom1 = el1.get_Geometry(opt1)
		enum = geom1.GetEnumerator()
		enum.MoveNext()
		geom2 = enum.Current.GetInstanceGeometry()
		enum2 = geom2.GetEnumerator()
		enum2.MoveNext()
		s1 = enum2.Current
		famdoc.Delete(satId)
		System.IO.File.Delete(sat_path)

		save_path = '%s%s.rfa' % (temp_path, name1)
		try: #set the category
			fam_cat = famdoc.Settings.Categories.get_Item(cat1.Name)
			famdoc.OwnerFamily.FamilyCategory = fam_cat
		except: pass
		s2 = FreeFormElement.Create(famdoc,s1)
		if isVoid1:
			void_par = s2.get_Parameter(BuiltInParameter.ELEMENT_IS_CUTTING).Set(1)
			void_par2 = famdoc.OwnerFamily.get_Parameter(BuiltInParameter.FAMILY_ALLOW_CUT_WITH_VOIDS).Set(1)
		else: #voids do not have a material values or a sub-cateogry
			if enable_mat:
				try:
					mat_fec = FilteredElementCollector(famdoc).OfClass(Material)
					for m in mat_fec:
						if m.Name == mat1:
							fam_mat = m
							break
					mat_par = s2.get_Parameter(BuiltInParameter.MATERIAL_ID_PARAM).Set(fam_mat.Id)
				except: pass
			if enable_subcat: #create and assign the sub-category:
				try:
					current_fam_cat = famdoc.OwnerFamily.FamilyCategory
					fam_cat_subs = current_fam_cat.SubCategories
					if fam_cat_subs.Contains(subcat1):
						new_subcat = fam_cat_subs[subcat1]
					else:
						new_subcat = famdoc.Settings.Categories.NewSubcategory(current_fam_cat, subcat1)
					s2.Subcategory = new_subcat
				except: pass
		TransactionManager.ForceCloseTransaction(t1)
		famdoc.SaveAs(save_path, SaveAsOpt)
		family1 = famdoc.LoadFamily(doc, FamOpt1() )
		famdoc.Close(False)
		System.IO.File.Delete(save_path)
		symbols = family1.GetFamilySymbolIds().GetEnumerator()
		symbols.MoveNext()
		symbol1 = doc.GetElement(symbols.Current)
		t1.EnsureInTransaction(doc)
		if not symbol1.IsActive: symbol1.Activate()
		inst1 = doc.Create.NewFamilyInstance(origin, symbol1, str_typ)
		ElementTransformUtils.MoveElement(doc,inst1.Id, vec1.Reverse().ToXyz() )
		TransactionManager.ForceCloseTransaction(t1)
		return inst1.ToDSType(False), family1.ToDSType(False)
		
	except:
		return traceback.format_exc(),''

if len(geom) == len(names) == len(category) == len(isVoid) == len(material) == len(subcat):
	return1 = map(NewForm_background, geom, names, category, isVoid, material, subcat)
elif len(geom) == len(names):
	padded = PadLists([geom, category, isVoid, material,subcat])
	p_category, p_isVoid, p_material, p_subcat = padded[1], padded[2], padded[3], padded[4]
	return1 = map(NewForm_background, geom, names, p_category, p_isVoid, p_material, p_subcat)
else : return1 = [('Make sure that each geometry\nobject has a unique family name.', '')]
OUT = [i[0] for i in return1], [i[1] for i in return1]
satOpt.Dispose()
opt1.Dispose()
SaveAsOpt.Dispose()