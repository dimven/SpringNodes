#-Reope----------------------------------------#
#                                              #
#      Copyright(c) 2017, Dimitar Venkov       #
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
from itertools import repeat
import traceback
from System.Collections.Generic import *

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
import Autodesk.Revit.DB as RVT

def tolist(obj1):
    if isinstance(obj1, str): return [obj1]
    return obj1 if isinstance(obj1, list) else [obj1]

def PadLists(lists):
    len1 = len(lists[0])
    for i in range(1, len(lists)):
        len2 = len(lists[i])
        if len2 == len1: continue
        elif len2 > len1: lists[i] = lists[i][:len1]
        else: lists[i].extend(repeat(lists[i][-1], len1 - len2))
    return lists
    
def NewDS(s1, cat1, name1):
    temp_path = System.IO.Path.GetTempPath()
    sat_path = "%s%s.sat" % (temp_path, name1)
    try:
        if factor != 1:
            s1 = s1.Scale(factor)
        sat1 = Geometry.ExportToSAT([s1], sat_path)
        satId = doc.Import(sat1, satOpt, view1)
        el1 = doc.GetElement(satId)
        geom1 = el1.get_Geometry(opt1)
        enum = geom1.GetEnumerator()
        enum.MoveNext()
        geom2 = enum.Current.GetInstanceGeometry()
        enum2 = geom2.GetEnumerator()
        enum2.MoveNext()
        s1 = enum2.Current
        doc.Delete(List[RVT.ElementId]([satId]))
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
                ds1 = RVT.DirectShape.CreateElementInstance(doc, old_type.Id, cat1Id, name1, tf1)
                ds1.SetTypeId(old_type.Id)
        else:
            dsType1 = RVT.DirectShapeType.Create(doc, name1, cat1Id)
            dsType1.SetShape([s1])
            dsLib.AddDefinitionType(name1, dsType1.Id)
            dst_enum[name1] = dsType1
            ds1 = RVT.DirectShape.CreateElementInstance(doc, dsType1.Id, cat1Id, name1, tf1)
            ds1.SetTypeId(dsType1.Id)

        return ueWrapper.Invoke(None, (ds1, False))
    except:
        return traceback.format_exc()

try:
    solids = tolist(IN[0])
    cat = [UnwrapElement(c) for c in tolist(IN[1])]
    names = tolist(IN[2])

    satOpt = RVT.SATImportOptions()
    satOpt.Placement = RVT.ImportPlacement.Origin
    satOpt.Unit = RVT.ImportUnit.Foot
    opt1 = RVT.Options()
    opt1.ComputeReferences = True

    acceptable_views = [RVT.ViewType.Elevation, RVT.ViewType.Section]
    view_fec = RVT.FilteredElementCollector(doc).OfClass(RVT.View)
    view1 = None
    for v in view_fec:
        if v.ViewType in acceptable_views and not v.IsTemplate:
            view1 = v
            break

    units = doc.GetUnits().GetFormatOptions(RVT.SpecTypeId.Length).GetUnitTypeId()
    factor = RVT.UnitUtils.ConvertToInternalUnits(1, units)

    dsLib = RVT.DirectShapeLibrary.GetDirectShapeLibrary(doc)
    tf1 = RVT.Transform.Identity

    dst_fec = RVT.FilteredElementCollector(doc).OfClass(RVT.DirectShapeType)
    dst_enum = dict((RVT.Element.Name.__get__(i), i) for i in dst_fec)

    ueWrapper = None
    wrappers = clr.GetClrType(Revit.Elements.ElementWrapper).GetMethods()
    for w in wrappers:
        if w.ToString().startswith("Revit.Elements.UnknownElement"):
            ueWrapper = w
            break

    if len(solids) == len(names):
        if not len(solids) == len(cat):
            padded = PadLists([solids, cat])
            cat = padded[1]
        TransactionManager.Instance.EnsureInTransaction(doc)
        
        tempSection = None
        if not view1:
            bb = RVT.BoundingBoxXYZ()
            bb.Min = RVT.XYZ.Zero
            bb.Max = RVT.XYZ(10, 10, 10)
            dst_fec2 = RVT.FilteredElementCollector(doc).OfClass(RVT.ViewFamilyType).WhereElementIsElementType()
            family = next((x for x in dst_fec2 if x.ViewFamily == RVT.ViewFamily.Section), None)
            if family:
                tempSection = RVT.ViewSection.CreateSection(doc, family.Id, bb)
                view1 = tempSection    
        
        OUT = list(map(NewDS, solids, cat, names))
        if tempSection:
            doc.Delete(tempSection.Id)        
        TransactionManager.Instance.TransactionTaskDone()
    else:
        OUT = "Make sure that each geometry\nobject has a unique type name."

    satOpt.Dispose()
    opt1.Dispose()

except Exception as e:
    OUT = "Exception:\n{0}\n\nTraceback:\n{1}".format(
        str(e),
        traceback.format_exc()
    )