#-Reope----------------------------------------#
#                                              #
#      Copyright(c) 2016, Dimitar Venkov       #
#                                              #
# https://github.com/dimven/SpringNodes/issues #
# https://www.reope.com/                       #
#                                              #
#    ____    _____   _____   ____    _____     #
#   |  _ \ *|  ___|*|  _  |*|  _ \ *|  ___|    #
#   | |_) |*| |___ *| | | |*| |_) |*| |___     #
#   |  _ < *|  ___|*| | | |*|  __/ *|  ___|    #
#   | | | |*| |___ *| |_| |*| |    *| |___     #
#   |_| \_|*|_____|*|_____|*|_|    *|_____|    #
#                                              #
#                                              #
#-Reope-----Updated by Mark Ackerley-----------#

import clr
import System
from System.Collections.Generic import *
from itertools import repeat
import uuid
import traceback

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Geometry as DynGeom
from Autodesk.DesignScript.Geometry import Point as DynPoint
from Autodesk.DesignScript.Geometry import Vector, BoundingBox

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import (
    FilteredElementCollector, Family, SaveAsOptions,
    FreeFormElement, BuiltInParameter, Material,
    ElementId, UnitUtils, XYZ, ElementTransformUtils,
    ForgeTypeId, IFamilyLoadOptions, ShapeImporter
)
from Autodesk.Revit.DB.Structure import StructuralType

doc = DocumentManager.Instance.CurrentDBDocument

def tolist(obj1):
    if isinstance(obj1, str): return [obj1]
    return obj1 if isinstance(obj1, list) else [obj1]

def PadLists(lists):
    len1 = len(lists[0])
    for i in range(1, len(lists)):
        len2 = len(lists[i])
        if len2 == len1:
            continue
        elif len2 > len1:
            lists[i] = lists[i][:len1]
        else:
            lists[i].extend(repeat(lists[i][-1], len1 - len2))
    return lists

class FamOpt1(IFamilyLoadOptions):
    __namespace__ = "FamOpt_" + str(uuid.uuid4()).replace('-', '')
    def __init__(self): super().__init__()
    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        overwriteParameterValues = True
        return (True, overwriteParameterValues)
    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        overwriteParameterValues = True
        return (True, overwriteParameterValues)

geom      = tolist(IN[0])
fam_path  = IN[1]
names     = tolist(IN[2])
category  = tolist(IN[3])
material  = tolist(IN[4])
mat_param = tolist(IN[5])
isVoid    = [str(x).lower() == 'true' for x in tolist(IN[6])]
subcat    = tolist(IN[7])

if int(doc.Application.VersionNumber) > 2021:
    units = doc.GetUnits().GetFormatOptions(ForgeTypeId("autodesk.spec.aec:length")).GetUnitTypeId()
else:
    units = doc.GetUnits().GetFormatOptions(UnitType.UT_Length).DisplayUnits

factor        = UnitUtils.ConvertToInternalUnits(1, units)
origin        = XYZ.Zero
str_typ       = StructuralType.NonStructural
t1            = TransactionManager.Instance
temp_path     = System.IO.Path.GetTempPath()
invalid_chars = System.IO.Path.GetInvalidFileNameChars()
SaveAsOpt     = SaveAsOptions()
SaveAsOpt.OverwriteExistingFile = True

def NewForm_background(s1, name1, cat1, isVoid1, mat1, mat_param1, subcat1):
    try:
        if mat1 is not None and mat_param1 is not None:
            return 'Provide material name (to hard-set) or parameter name (to associate), not both', ''

        if not isinstance(name1, str):
            return 'Expected a string for family name, got %s' % type(name1).__name__, ''

        if any(c in name1 for c in invalid_chars):
            raise Exception('Family name contains invalid characters')

        s1 = list(s1) if hasattr(s1, '__iter__') and not isinstance(s1, str) else [s1]

        existing = next(
            (f for f in FilteredElementCollector(doc).OfClass(Family)
             if f.Name == name1),
            None
        )
        if existing is not None:
            return 'Family "%s" already exists - rename or delete it first' % name1, ''

        enable_mat    = mat1      is not None
        enable_param  = mat_param1 is not None
        enable_subcat = subcat1   is not None

        TransactionManager.ForceCloseTransaction(t1)
        famdoc = doc.Application.NewFamilyDocument(fam_path)

        fam_mat_id = None
        if enable_mat:
            for m in FilteredElementCollector(famdoc).OfClass(Material):
                if m.Name == mat1:
                    fam_mat_id = m.Id
                    break
            if fam_mat_id is None:
                famdoc.Close(False)
                return 'Material "%s" not found in family template' % mat1, ''

        sat_path = '%s%s.sat' % (temp_path, name1)

        if factor != 1:
            s1 = [x.Scale(factor) for x in s1]

        vec1 = Vector.ByTwoPoints(BoundingBox.ByGeometry(s1).MinPoint, DynPoint.Origin())
        s1   = [x.Translate(vec1) for x in s1]
        sat1 = DynGeom.ExportToSAT(s1, sat_path)

        t1.EnsureInTransaction(famdoc)
        solids = ShapeImporter().Convert(famdoc, sat1)
        System.IO.File.Delete(sat_path)

        save_path = '%s%s.rfa' % (temp_path, name1)

        try:
            famdoc.OwnerFamily.FamilyCategory = famdoc.Settings.Categories.get_Item(cat1.Name)
        except Exception:
            pass

        new_subcat = None
        if enable_subcat:
            try:
                fam_cat      = famdoc.OwnerFamily.FamilyCategory
                fam_cat_subs = fam_cat.SubCategories
                new_subcat   = fam_cat_subs[subcat1] if fam_cat_subs.Contains(subcat1) \
                               else famdoc.Settings.Categories.NewSubcategory(fam_cat, subcat1)
            except Exception:
                pass

        fam_param = None
        if enable_param:
            fam_param = next(
                (p for p in famdoc.FamilyManager.Parameters
                 if p.Definition.Name == mat_param1),
                None
            )
            if fam_param is None:
                famdoc.Close(False)
                return 'Family parameter "%s" not found in template' % mat_param1, ''

        allow_cut_set = False
        for solid in solids:
            s2 = FreeFormElement.Create(famdoc, solid)
            if isVoid1:
                s2.get_Parameter(BuiltInParameter.ELEMENT_IS_CUTTING).Set(1)
                if not allow_cut_set:
                    famdoc.OwnerFamily.get_Parameter(BuiltInParameter.FAMILY_ALLOW_CUT_WITH_VOIDS).Set(1)
                    allow_cut_set = True
            else:
                s2.get_Parameter(BuiltInParameter.ELEMENT_IS_CUTTING).Set(0)
                if fam_mat_id is not None:
                    p = s2.LookupParameter("Material")
                    if p is not None:
                        try:
                            p.Set(fam_mat_id)
                        except Exception:
                            pass
                if fam_param is not None:
                    elem_mat_p = s2.LookupParameter("Material")
                    if elem_mat_p is not None:
                        try:
                            famdoc.FamilyManager.AssociateElementParameterToFamilyParameter(elem_mat_p, fam_param)
                        except Exception:
                            pass
                if new_subcat is not None:
                    try:
                        s2.Subcategory = new_subcat
                    except Exception:
                        pass

        TransactionManager.ForceCloseTransaction(t1)
        famdoc.SaveAs(save_path, SaveAsOpt)
        family1 = famdoc.LoadFamily(doc, FamOpt1())
        famdoc.Close(False)
        System.IO.File.Delete(save_path)

        symbols = family1.GetFamilySymbolIds().GetEnumerator()
        symbols.MoveNext()
        symbol1 = doc.GetElement(symbols.Current)

        t1.EnsureInTransaction(doc)
        if not symbol1.IsActive:
            symbol1.Activate()
        inst1 = doc.Create.NewFamilyInstance(origin, symbol1, str_typ)
        ElementTransformUtils.MoveElement(doc, inst1.Id, XYZ(-vec1.X, -vec1.Y, -vec1.Z))
        TransactionManager.ForceCloseTransaction(t1)

        return inst1, family1

    except Exception:
        return traceback.format_exc(), ''

# Dispatch
if len(geom) == len(names) == len(category) == len(isVoid) == len(material) == len(mat_param) == len(subcat):
    return1 = list(map(NewForm_background, geom, names, category, isVoid, material, mat_param, subcat))
elif len(geom) == len(names):
    padded  = PadLists([geom, category, isVoid, material, mat_param, subcat])
    return1 = list(map(NewForm_background, geom, names, padded[1], padded[2], padded[3], padded[4], padded[5]))
elif len(names) == 1:
    return1 = [NewForm_background(geom, names[0], category[0], isVoid[0], material[0], mat_param[0], subcat[0])]
else:
    return1 = [('Make sure each geometry entry has exactly one family name.', '')]

OUT = [i[0] for i in return1], [i[1] for i in return1]
SaveAsOpt.Dispose()