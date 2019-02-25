#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr
from itertools import repeat

clr.AddReference('System')
import System
from System.Collections.Generic import List

pf_path = System.Environment.GetFolderPath(System.Environment.SpecialFolder.ProgramFilesX86)
import sys
sys.path.append('%s\IronPython 2.7\Lib' %pf_path)
import traceback

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument
app = DocumentManager.Instance.CurrentUIApplication.Application

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

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
	def __init__(self): pass
	def OnFamilyFound(self,familyInUse, overwriteParameterValues):
		return True
	def OnSharedFamilyFound(self,familyInUse, source, overwriteParameterValues):
		return True

def vert1(obj1) : return [v.PointGeometry for v in obj1.Vertices]

def tup1(p) : return round(p.X,3), round(p.Y,3), round(p.Z,3)

def domain1(c1, c2, d1):
	x = 1.0 - abs(c1 - c2) / d1
	return 1 if x > 1 else 0 if x < 0 else x

class PtsErrorMuncher(IFailuresPreprocessor):
	def PreprocessFailures(self, fa):
		failList = List[FailureMessageAccessor](fa.GetFailureMessages() )
		for failure in failList:
			failID = failure.GetFailureDefinitionId()
			if failID == BuiltInFailures.InaccurateFailures.InaccurateLine\
			or failID == BuiltInFailures.OverlapFailures.DuplicatePoints :
				fa.DeleteWarning(failure)
		return FailureProcessingResult.Continue

geom = tolist(IN[0])
fam_path = IN[1]
names = tolist(IN[2])
category = tolist(IN[3])
material = tolist(IN[4])
subcat = tolist(IN[5])

temp_path = System.IO.Path.GetTempPath()
pmt = PointOnCurveMeasurementType.NormalizedCurveParameter
pmf = PointOnCurveMeasureFrom.Beginning

TransactionManager.ForceCloseTransaction(TransactionManager.Instance)

def NewAC_background(s1, name1, cat1, mat1, subcat1):
	try:
		enable_mat = True
		if mat1 == None: enable_mat = False
		enable_subcat = True
		if subcat1 == None: enable_subcat = False

		bb1 = s1.BoundingBox
		cub1 = bb1.ToCuboid()
		sizes1 = cub1.Width, cub1.Length, cub1.Height
		orig1 = tup1(bb1.MinPoint)

		cub_corners = vert1(cub1)
		cub_corners = [cub_corners[n:n+2] for n in xrange(0,8,2)]
		cub_corners[1].reverse()
		cub_corners[2].reverse()

		s1_corners = map(tup1, vert1(s1) )
		dist1 = [map(domain1, orig1, s1_corners[i], sizes1)\
		for i in xrange(len(s1_corners) )]
		par2, par1, par3 = zip(*dist1)

		face_corners = [map(tup1,f) for f in map(vert1,s1.Faces)]
		#End of Dynamo geometry pre-processing

		a_pts = [ [p.ToXyz(True) for p in pts] for pts in cub_corners]
		famdoc = doc.Application.NewFamilyDocument(fam_path)
		factory = famdoc.FamilyCreate
		def ref_line(pts, factory = factory):
			pt_arr = ReferencePointArray()
			pt_arr.Append(pts[0])
			pt_arr.Append(pts[1])
			l1 = factory.NewCurveByPoints(pt_arr)
			l1.IsReferenceLine = True
			l1.ReferenceType = ReferenceType.None
			return l1

		def ref_pt(l1, par1, pmt = pmt, pmf = pmf, factory = factory, app = app.Create):
			loc1 = PointLocationOnCurve(pmt, par1, pmf)
			ref1 = l1.GeometryCurve.Reference
			pt_ref = app.NewPointOnEdge(ref1, loc1)
			return factory.NewReferencePoint(pt_ref)

		def adp_pt(p1, factory = factory):
			pt1 = factory.NewReferencePoint(p1)
			par1 = pt1.get_Parameter(BuiltInParameter.POINT_ADAPTIVE_TYPE_PARAM)
			par1.Set(1)
			return pt1

		xr1 = xrange(4)
		len1 = len(par1)
		xr2 = xrange(len1)
		with Transaction(famdoc,' ') as t:
			t.Start()
			# Catch annoyng points same location warning
			failOptions = t.GetFailureHandlingOptions()
			failOptions.SetFailuresPreprocessor(PtsErrorMuncher())
			t.SetFailureHandlingOptions(failOptions)

			a_pts1 = [map(adp_pt, pts) for pts in a_pts]
			famdoc.Regenerate()
			lines1 = [ref_line(a_pts1[i]) for i in xr1]
			pts1 = [ [ref_pt(lines1[i],par1[j]) for j in xr2] for i in xr1]
			pts1z = zip(*pts1[:2]) + zip(*pts1[2:])
			famdoc.Regenerate()
			lines2 = [ref_line(pts1z[i]) for i in xrange(len(pts1z) )]
			lines2z = zip(lines2[:len1],lines2[len1:])
			pts2 = [ [ref_pt(lines2z[i][j],par2[i]) for j in xrange(2)] for i in xr2]
			famdoc.Regenerate()
			lines3 = map(ref_line, pts2)
			pts3 = [ref_pt(lines3[i],par3[i]) for i in xr2]
			famdoc.Regenerate()
			#End of reference skeleton construction

			face_refs = []
			ref_dict = dict(zip(s1_corners,pts3))
			def search1(searchVals):
				refs1 = []
				for i in xrange(len(searchVals) ):
					if searchVals[i] in ref_dict:
						refs1.append(ref_dict[searchVals[i]])
					else : pass
				face_refs.append(refs1)
			map(search1, face_corners)
			#End of face reference mapping

			faces = []
			for ref in face_refs:
				refArr = ReferenceArray()
				for i in xrange(-1,len(ref) - 1) :
					ii = i+1
					c1 = ref_line( (ref[i],ref[ii]) )
					r1 = Reference(c1)
					refArr.Insert(r1,ii)
				f1 = factory.NewFormByCap(True, refArr)
				faces.append(f1)
			#End of face generation section

			famdoc.Regenerate()
			try: #set the family category
				fam_cat = famdoc.Settings.Categories.get_Item(cat1.Name)
				famdoc.OwnerFamily.FamilyCategory = fam_cat
			except: pass
			if enable_mat: #assign a material to the family
				fam_mat = None
				mat_fec = FilteredElementCollector(famdoc).OfClass(Material)
				for m in mat_fec:
					if m.Name == mat1:
						fam_mat = m.Id
						break
				if fam_mat != None:
					for f in faces:
						mat_par = f.get_Parameter(BuiltInParameter.MATERIAL_ID_PARAM)
						mat_par.Set(fam_mat)
			if enable_subcat: #create and assign the sub-category:
				try:
					cur_fam_cat = famdoc.OwnerFamily.FamilyCategory
					new_subcat = famdoc.Settings.Categories.NewSubcategory(cur_fam_cat, subcat1)
					for f in faces: f.Subcategory = new_subcat
				except: pass
			t.Commit()
		save_path = '%s%s.rfa' % (temp_path, name1)
		SaveAsOpt = SaveAsOptions() #should probably dispose of these
		SaveAsOpt.OverwriteExistingFile = True
		famdoc.SaveAs(save_path, SaveAsOpt)
		family1 =  famdoc.LoadFamily(doc, FamOpt1())
		famdoc.Close(False)
		System.IO.File.Delete(save_path)
		symbols = family1.GetFamilySymbolIds().GetEnumerator()
		symbols.MoveNext()
		symbol1 = doc.GetElement(symbols.Current)
		#might need to activate the symbol
		return symbol1.ToDSType(False), family1.ToDSType(False)

	except: return traceback.format_exc(), ''

if len(geom) == len(names) == len(category) == len(material) == len(subcat):
	return1 = map(NewAC_background, geom, names, category, material, subcat)
elif len(geom) == len(names):
	padded = PadLists([geom, category, material,subcat])
	p_category, p_material, p_subcat = padded[1], padded[2], padded[3]
	return1 = map(NewAC_background, geom, names, p_category, p_material, p_subcat)
else : return1 = [('Make sure that each geometry\\nobject has a unique family name.', '')]

OUT = [i[0] for i in return1], [i[1] for i in return1]